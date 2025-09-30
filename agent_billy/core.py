from __future__ import annotations
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

from .utils import (
    WORKSPACE, PROJECTS_DIR, MEMORY_FILE,
    now_iso, load_memory, save_memory
)
from .git_ops import run_git, ensure_workspace_git


# ────────────────────────────────────────────────────────────────────────────────
# Internal helpers

def _write_new_file(project: str, version: str, file_path: Path, inline_content: Optional[str]) -> str:
    """
    Create a new version file from scratch (no auto-copy).
    Returns a human string describing how the file was seeded.
    """
    header = [
        "#!/usr/bin/env python3",
        f"# Project: {project}",
        f"# Version: {version}",
        f"# Created: {now_iso()}",
        "",
    ]
    if inline_content is None:
        body = (
            "def main():\n"
            f"    print('Hello from {project} {version}!')\n\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        )
    else:
        body = inline_content

    file_path.write_text("\n".join(header) + body, encoding="utf-8")
    os.chmod(file_path, 0o755)
    return "blank template" if inline_content is None else "inline content"


def _rewrite_header_for_copy(text: str, project: str, version: str) -> str:
    """
    When auto-copying a previous version, update the header lines for Version/Created if present.
    We only touch simple '# Key: value' header lines.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines[:6]):  # headers are right at the top
        if line.startswith("# Version:"):
            lines[i] = f"# Version: {version}"
        elif line.startswith("# Created:"):
            lines[i] = f"# Created: {now_iso()}"
        elif line.startswith("# Project:"):
            # keep the same project name, but enforce correctness
            lines[i] = f"# Project: {project}"
    return "\n".join(lines)


def _seed_from_previous(project_meta: Dict[str, Any], project: str, from_version: str, dest: Path) -> str:
    """Copy content from an existing version in the same project and refresh the header."""
    prev_meta = project_meta["versions"][from_version]
    prev_file = WORKSPACE / prev_meta["filename"]
    if not prev_file.exists():
        raise FileNotFoundError(f"Previous version file missing: {prev_file}")

    text = prev_file.read_text(encoding="utf-8")
    text = _rewrite_header_for_copy(text, project, dest.stem.split("_")[-1])  # update Version/Created
    dest.write_text(text, encoding="utf-8")
    # preserve executable bit if present on source
    src_mode = prev_file.stat().st_mode
    os.chmod(dest, src_mode)
    return f"auto-copied from {from_version}"


# ────────────────────────────────────────────────────────────────────────────────
# Public API called from CLI

def create_project(name: str, description: str = "", git_enabled: bool = False) -> int:
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
        "git_enabled": bool(git_enabled),
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


def list_projects(target: Optional[str] = None) -> int:
    memory = load_memory()
    projects = memory.get("projects", {})
    if not projects:
        print("ℹ️ No projects yet.")
        return 0

    if target:
        if target not in projects:
            print(f"❌ Project '{target}' not found.")
            return 1
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
    return 0


def add_version(
    project: str,
    version: str,
    description: str = "",
    from_version: Optional[str] = None,
    inline_content: Optional[str] = None,
) -> int:
    """
    Creates a file named <project>_<version>.py inside projects/<project>/,
    records it in memory.json, and if git is enabled commits + tags the change.
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

    # Decide how to seed the file
    if from_version:
        if from_version not in proj_meta.get("versions", {}):
            print(f"❌ Version '{from_version}' not found in project '{project}'.")
            return 1
        seed_info = _seed_from_previous(proj_meta, project, from_version, file_path)
        copied_from = from_version
    elif inline_content is not None:
        seed_info = _write_new_file(project, version, file_path, inline_content)
        copied_from = None
    else:
        versions = proj_meta.get("versions", {})
        if versions:
            last_v = sorted(versions.keys())[-1]
            seed_info = _seed_from_previous(proj_meta, project, last_v, file_path)
            copied_from = last_v
        else:
            seed_info = _write_new_file(project, version, file_path, None)
            copied_from = None

    # Update memory.json
    proj_meta["versions"][version] = {
        "filename": f"projects/{project}/{filename}",
        "created_at": now_iso(),
        "description": description,
        "copied_from": copied_from,
        "dependencies": [],
        "last_run": None,
        "notes": "",
        "git_commit": None,
    }
    save_memory(memory)

    # Git commit & tag
    if proj_meta.get("git_enabled"):
        if ensure_workspace_git(verbose=False):
            run_git(["add", f"projects/{project}/{filename}", "memory.json"])
            msg = f"{project} {version}: {description or 'New version'} ({seed_info})"
            run_git(["commit", "-m", msg])
            commit = run_git(["rev-parse", "HEAD"])
            # Tag with project_version
            run_git(["tag", f"{project}_{version}", commit])

            # persist commit hash
            memory = load_memory()
            memory["projects"][project]["versions"][version]["git_commit"] = commit
            save_memory(memory)
            print(
                f"✅ Version '{version}' added, committed, and tagged as {project}_{version}. "
                f"{seed_info}, commit={commit[:8]}"
            )
        else:
            print("⚠️ Git repo not initialized at workspace; skipping commit.")
    else:
        print(f"✅ Version '{version}' added ({seed_info}).")

    return 0


def run_version(project: str, version: str) -> int:
    memory = load_memory()
    try:
        meta = memory["projects"][project]["versions"][version]
    except KeyError:
        print(f"❌ Cannot find project='{project}' version='{version}'")
        return 1

    file_rel = meta["filename"]
    file_abs = WORKSPACE / file_rel
    if not file_abs.exists():
        print(f"❌ File missing on disk: {file_abs}")
        return 1

    print(f"▶️  Running: {file_rel}")
    code = subprocess.run([sys.executable, str(file_abs)]).returncode

    memory["projects"][project]["versions"][version]["last_run"] = now_iso()
    save_memory(memory)

    if code == 0:
        print("✅ Run finished OK.")
    else:
        print(f"⚠️ Run exited with code {code}")
    return code


def diff_versions(project: str, version1: str, version2: str) -> int:
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
