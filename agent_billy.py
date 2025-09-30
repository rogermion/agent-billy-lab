#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ────────────────────────────────────────────────────────────────────────────────
# Workspace constants
WORKSPACE = Path(__file__).resolve().parent
PROJECTS_DIR = WORKSPACE / "projects"
MEMORY_FILE = WORKSPACE / "memory.json"

# ────────────────────────────────────────────────────────────────────────────────
# Memory helpers

def now_iso():
    return datetime.now().isoformat(timespec="seconds")

def load_memory():
    if not MEMORY_FILE.exists():
        return {"projects": {}}
    with MEMORY_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    with MEMORY_FILE.open("w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

# ────────────────────────────────────────────────────────────────────────────────
# Git helpers

def git_passthrough(args):
    """Run a git command inside the workspace repo."""
    if not ensure_workspace_git(verbose=False):
        print("❌ No git repo in workspace.")
        return 1
    result = subprocess.run(
        ["git"] + args,
        cwd=str(WORKSPACE),
        text=True
    )
    return result.returncode

def run_git(args):
    try:
        result = subprocess.run(
            ["git"] + args, cwd=str(WORKSPACE),
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"⚠️ git {' '.join(args)} failed:\n{e.stderr}")
        return None

def workspace_git_ready():
    return (WORKSPACE / ".git").exists()

def ensure_workspace_git(verbose=True):
    if not workspace_git_ready():
        out = run_git(["init"])
        if verbose:
            print("✅ Initialized git repository at workspace root.")
        return out is not None
    return True

# ────────────────────────────────────────────────────────────────────────────────
# Core ops

def create_project(name, description="", git_enabled=False):
    memory = load_memory()

    if name in memory["projects"]:
        print(f"❌ Project '{name}' already exists.")
        return 1

    PROJECTS_DIR.mkdir(exist_ok=True)
    project_path = PROJECTS_DIR / name
    project_path.mkdir(parents=True, exist_ok=True)

    memory["projects"][name] = {
        "created_at": now_iso(),
        "description": description,
        "versions": {},
        "tags": [],
        "git_enabled": bool(git_enabled)
    }
    save_memory(memory)

    print(f"✅ Project '{name}' created at {project_path} (git_enabled={git_enabled}).")

    if git_enabled:
        if ensure_workspace_git():
            run_git(["add", "memory.json", f"projects/{name}/"])
            run_git(["commit", "-m", f"Create project {name}"])
        else:
            print("⚠️ Git not initialized at workspace root; run `git init` then commit.")
    return 0

def list_projects(target=None):
    memory = load_memory()
    projects = memory.get("projects", {})
    if not projects:
        print("ℹ️ No projects yet.")
        return

    if target:
        if target not in projects:
            print(f"❌ Project '{target}' not found.")
            return
        p = projects[target]
        print(f"📦 {target} — created {p['created_at']}")
        print(f"   description: {p.get('description','')}")
        print(f"   git_enabled: {p.get('git_enabled', False)}")
        vers = p.get("versions", {})
        if not vers:
            print("   versions: (none)")
        else:
            print("   versions:")
            for v, meta in sorted(vers.items()):
                print(f"    - {v} → {meta['filename']} (created {meta['created_at']})")
    else:
        print("📚 Projects:")
        for name, p in projects.items():
            n_versions = len(p.get("versions", {}))
            print(f" - {name} (versions: {n_versions}, created {p['created_at']})")

def add_version(project, version, description="", copied_from=None, dependencies=None,
                from_file=None, inline_content=None, from_version=None):
    """
    Creates a file named <project>_<version>.py inside projects/<project>/,
    records it in memory.json, commits it, and tags the commit.
    """
    memory = load_memory()
    if project not in memory["projects"]:
        print(f"❌ Project '{project}' not found.")
        return 1

    proj_meta = memory["projects"][project]
    project_path = PROJECTS_DIR / project
    project_path.mkdir(parents=True, exist_ok=True)

    filename = f"{project}_{version}.py"
    file_path = project_path / filename

    # ── Decide how to seed the file ─────────────────────────────────────────────
    if from_file:
        src = Path(from_file).expanduser().resolve()
        if not src.exists():
            print(f"❌ --from-file path not found: {src}")
            return 1
        shutil.copyfile(src, file_path)
        seed_info = f"from external file {src}"

    elif from_version:
        try:
            prev_meta = proj_meta["versions"][from_version]
            prev_file = WORKSPACE / prev_meta["filename"]
            if not prev_file.exists():
                print(f"❌ Cannot find previous version file: {prev_file}")
                return 1
            shutil.copyfile(prev_file, file_path)
            seed_info = f"auto-copied from {from_version}"
            copied_from = from_version
        except KeyError:
            print(f"❌ Version '{from_version}' not found in project '{project}'.")
            return 1

    elif inline_content:
        header = [
            "#!/usr/bin/env python3",
            f"# Project: {project}",
            f"# Version: {version}",
            f"# Created: {now_iso()}",
            "",
        ]
        file_path.write_text("\n".join(header) + inline_content, encoding="utf-8")
        os.chmod(file_path, 0o755)
        seed_info = "inline content"

    else:
        # Default: copy from latest version if available
        versions = proj_meta.get("versions", {})
        if versions:
            last_version = sorted(versions.keys())[-1]
            prev_file = WORKSPACE / proj_meta["versions"][last_version]["filename"]
            shutil.copyfile(prev_file, file_path)
            copied_from = last_version
            seed_info = f"auto-copied from latest ({last_version})"
        else:
            # fallback: blank template
            header = [
                "#!/usr/bin/env python3",
                f"# Project: {project}",
                f"# Version: {version}",
                f"# Created: {now_iso()}",
                "",
                "def main():",
                f"    print('Hello from {project} {version}!')",
                "",
                "if __name__ == '__main__':",
                "    main()",
            ]
            file_path.write_text("\n".join(header), encoding="utf-8")
            os.chmod(file_path, 0o755)
            seed_info = "blank template"

    # ── Update memory.json ──────────────────────────────────────────────────────
    if dependencies is None:
        dependencies = []

    proj_meta["versions"][version] = {
        "filename": f"projects/{project}/{filename}",
        "created_at": now_iso(),
        "description": description,
        "copied_from": copied_from,
        "dependencies": dependencies,
        "last_run": None,
        "notes": "",
        "git_commit": None
    }
    save_memory(memory)

    # ── Git commit & tag ────────────────────────────────────────────────────────
    if proj_meta.get("git_enabled"):
        if ensure_workspace_git(verbose=False):
            run_git(["add", f"projects/{project}/{filename}", "memory.json"])
            msg = f"{project} {version}: {description or 'New version'} ({seed_info})"
            run_git(["commit", "-m", msg])
            commit = run_git(["rev-parse", "HEAD"])
            # Tagging this commit
            run_git(["tag", f"{project}_{version}", commit])

            # persist commit hash
            memory = load_memory()
            memory["projects"][project]["versions"][version]["git_commit"] = commit
            save_memory(memory)
            print(f"✅ Version '{version}' added, committed, and tagged as {project}_{version}. {seed_info}, commit={commit[:8]}")
        else:
            print("⚠️ Git repo not initialized at workspace; skipping commit.")
    else:
        print(f"✅ Version '{version}' added ({seed_info}).")

    return 0

def run_version(project, version):
    memory = load_memory()
    try:
        meta = memory["projects"][project]["versions"][version]
    except KeyError:
        print(f"❌ Cannot find {project=} {version=}")
        return 1

    file_rel = meta["filename"]
    file_abs = WORKSPACE / file_rel
    if not file_abs.exists():
        print(f"❌ File missing on disk: {file_abs}")
        return 1

    print(f"▶️  Running: {file_rel}")
    proc = subprocess.run([sys.executable, str(file_abs)])
    code = proc.returncode

    memory["projects"][project]["versions"][version]["last_run"] = now_iso()
    save_memory(memory)

    if code == 0:
        print("✅ Run finished OK.")
    else:
        print(f"⚠️ Run exited with code {code}")
    return code

def diff_versions(project, version1, version2):
    """Show git diff between two versions of a project."""
    memory = load_memory()
    proj = memory["projects"].get(project)
    if not proj:
        print(f"❌ Project '{project}' not found.")
        return 1

    v1 = proj["versions"].get(version1)
    v2 = proj["versions"].get(version2)
    if not v1 or not v2:
        print(f"❌ One of the versions not found ({version1}, {version2}).")
        return 1

    commit1 = v1.get("git_commit")
    commit2 = v2.get("git_commit")
    if not commit1 or not commit2:
        print("⚠️ Missing commit hashes, cannot diff.")
        return 1

    print(f"🔍 Diff between {version1} ({commit1[:8]}) and {version2} ({commit2[:8]}):\n")
    diff = run_git(["diff", f"{commit1}", f"{commit2}"])
    if diff:
        print(diff)
    else:
        print("ℹ️ No differences found.")
    return 0

# ────────────────────────────────────────────────────────────────────────────────
# CLI

def main():
    parser = argparse.ArgumentParser(
        prog="Agent Billy",
        description="Local Python-based project/version manager with Git commits, tags, and diffs."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create", help="Create a new project")
    p_create.add_argument("project")
    p_create.add_argument("-d", "--description", default="", help="Project description")
    p_create.add_argument("--git", action="store_true", help="Enable Git commits for this project")

    p_list = sub.add_parser("list", help="List projects or versions of a project")
    p_list.add_argument("project", nargs="?", help="Project name (optional)")

    p_gitcmd = sub.add_parser("git", help="Run raw git commands inside workspace")
    p_gitcmd.add_argument("git_args", nargs=argparse.REMAINDER)

    p_save = sub.add_parser("save-version", help="Save a new version (creates file + memory + commit + tag)")
    p_save.add_argument("project")
    p_save.add_argument("version")
    p_save.add_argument("-m", "--message", default="", help="Version description (commit message body)")
    p_save.add_argument("--copied-from", default=None, help="Record lineage manually")
    p_save.add_argument("--deps", default="", help="Comma-separated dependencies to record")
    src = p_save.add_mutually_exclusive_group()
    src.add_argument("--from-file", default=None, help="Seed content from an existing file")
    src.add_argument("--content", default=None, help="Inline content string for the version file")
    p_save.add_argument("--from-version", default=None, help="Copy content from an existing version")

    p_run = sub.add_parser("run", help="Run a specific version")
    p_run.add_argument("project")
    p_run.add_argument("version")

    p_git = sub.add_parser("init-git", help="Initialize workspace git repo")

    p_diff = sub.add_parser("diff", help="Show diff between two versions")
    p_diff.add_argument("project")
    p_diff.add_argument("version1")
    p_diff.add_argument("version2")

    args = parser.parse_args()

    if args.cmd == "git":
        return git_passthrough(args.git_args)

    if args.cmd == "create":
        return create_project(args.project, args.description, args.git)

    if args.cmd == "list":
        return list_projects(args.project)

    if args.cmd == "save-version":
        deps = [d.strip() for d in args.deps.split(",")] if args.deps else []
        return add_version(
            project=args.project,
            version=args.version,
            description=args.message,
            copied_from=args.copied_from,
            dependencies=deps,
            from_file=args.from_file,
            inline_content=args.content,
            from_version=args.from_version
        )

    if args.cmd == "run":
        return run_version(args.project, args.version)

    if args.cmd == "init-git":
        ok = ensure_workspace_git()
        if ok:
            print("✅ Workspace git ready.")
        else:
            print("❌ Could not initialize git.")
        return 0

    if args.cmd == "diff":
        return diff_versions(args.project, args.version1, args.version2)

if __name__ == "__main__":
    sys.exit(main())
