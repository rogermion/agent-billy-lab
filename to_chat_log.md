# To Chat Log — agent_billy
Generated: 2025-09-30T20:50:59

**Description:** Local Python-based project manager agent

**Git enabled:** True

**Workspace:** /Users/macproroger/Documents/PROGRAMMING/agent-billy-lab
**Python:** 3.12.3

---

## Repo Status
## main...origin/main

## Recent Commits
f1d3d1d Add test-cycle integration into chat-log and full Billy source snapshot
203410e agent_billy v8: Sanity test version (auto-copied from v7)
8e1cd6f Remove legacy monolithic script agent_billy.py
ba275dc Refactor: split into package (core, git_ops, log, cli)
10713c9 agent_billy log: docs: update Stage 1 log

## Tags
agent_billy_v4
agent_billy_v5
agent_billy_v6
agent_billy_v7
agent_billy_v8

---

## Versions
- v1: Initial skeleton (created 2025-09-30T16:27:20)
  - file: projects/agent_billy/agent_billy_v1.py
  - copied_from: None
  - git_commit: 8447a8e6d6ca9b277ae3a32b25a9318b17fce505
  - last_run: None

```python
#!/usr/bin/env python3
# Project: agent_billy
# Version: v1
# Created: 2025-09-30T16:27:20

def main():
    print('Hello from agent_billy v1!')

if __name__ == '__main__':
    main()
```

- v2: Tweaked functions (created 2025-09-30T16:27:36)
  - file: projects/agent_billy/agent_billy_v2.py
  - copied_from: v1
  - git_commit: 42e0e31a41ef6900329ba4be9ecf87c1b0407fa5
  - last_run: 2025-09-30T16:28:03

```python
#!/usr/bin/env python3
# Project: agent_billy
# Version: v1
# Created: 2025-09-30T16:27:20

def main():
    print('Hello from agent_billy v1!')

if __name__ == '__main__':
    main()
```

- v3: Branch off v1 (created 2025-09-30T16:27:53)
  - file: projects/agent_billy/agent_billy_v3.py
  - copied_from: v1
  - git_commit: 244476801b8d7b1b07b15bc0b450df63988f1bb1
  - last_run: None

```python
#!/usr/bin/env python3
# Project: agent_billy
# Version: v1
# Created: 2025-09-30T16:27:20

def main():
    print('Hello from agent_billy v1!')

if __name__ == '__main__':
    main()
```

- v4: Custom experiment (created 2025-09-30T16:27:58)
  - file: projects/agent_billy/agent_billy_v4.py
  - copied_from: None
  - git_commit: c13a9f286d25d816cc422b77cb586236ae68e45f
  - last_run: None

```python
#!/usr/bin/env python3
# Project: agent_billy
# Version: v4
# Created: 2025-09-30T16:27:58
print('Hello v4!')
```

- v5: Testing Git tags and diff (created 2025-09-30T16:39:47)
  - file: projects/agent_billy/agent_billy_v5.py
  - copied_from: v4
  - git_commit: 00b15800a9eadca5f975813f7fa35a5e5adae669
  - last_run: None

```python
#!/usr/bin/env python3
# Project: agent_billy
# Version: v4
# Created: 2025-09-30T16:27:58
print('Hello v4!')
```

- v6: End-to-end GitHub sync test (created 2025-09-30T17:00:04)
  - file: projects/agent_billy/agent_billy_v6.py
  - copied_from: None
  - git_commit: c8d45baa16d915f63371fbaef4f280432b04b1b0
  - last_run: 2025-09-30T17:01:47

```python
#!/usr/bin/env python3
# Project: agent_billy
# Version: v6
# Created: 2025-09-30T17:00:04
print('Hello from v6!')
```

- v7: Refactor: modular core + git helpers (created 2025-09-30T18:48:21)
  - file: projects/agent_billy/agent_billy_v7.py
  - copied_from: v6
  - git_commit: 280075171e79380f0e49ec1356b75fe5f259cdc8
  - last_run: 2025-09-30T18:48:34

```python
#!/usr/bin/env python3
# Project: agent_billy
# Version: v7
# Created: 2025-09-30T18:48:21
print('Hello from v6!')
```

- v8: Sanity test version (created 2025-09-30T19:03:17)
  - file: projects/agent_billy/agent_billy_v8.py
  - copied_from: v7
  - git_commit: 203410e451d193e3bb95b707fc7c0d7bc78088a6
  - last_run: 2025-09-30T19:36:41

```python
#!/usr/bin/env python3
# Project: agent_billy
# Version: v8
# Created: 2025-09-30T19:03:17
print('Hello from v6!')
```

## Project Log
# agent_billy Log

- [2025-09-30T18:56:56] Step 1A validated ✅ on Chrome – Hello World displayed
- [2025-09-30T18:57:56] docs: update Stage 1 log
- [2025-09-30T19:03:42] Sanity test log entry

---

## Health Warnings
All versions have git commits ✅
- Latest version (v8) was run ✅
- Project log present ✅

---

# Test Cycle Results for agent_billy

### Step 1 — List Project
✅ Project listed successfully.

### Step 2 — Run Latest Version
✅ Ran latest version (v8) successfully.

### Step 3 — Git Status
```
## main...origin/main
 M memory.json
```


---

## Billy Source Snapshot
### billy.py
```python
#!/usr/bin/env python3
from agent_billy.cli import main

if __name__ == "__main__":
    main()
```

### agent_billy/__init__.py
```python

```

### agent_billy/chatlog.py
```python
# agent_billy/chatlog.py
import sys
from datetime import datetime
from pathlib import Path
import subprocess
import json

from .core import list_projects, run_version
from .utils import WORKSPACE, MEMORY_FILE

DOCS_DIR = WORKSPACE / "docs"


def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def run_git(args):
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=str(WORKSPACE),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


# ────────────────────────────────────────────────────────────────────────────────
# Test Cycle Helper
def run_test_cycle(project: str) -> list[str]:
    """Run a simple test cycle: list project, run latest version, check git status."""
    results = []
    results.append(f"# Test Cycle Results for {project}\n")

    # Step 1: List project
    results.append("### Step 1 — List Project")
    try:
        list_projects(project)
        results.append("✅ Project listed successfully.\n")
    except Exception as e:
        results.append(f"⚠️ Error listing project: {e}\n")

    # Step 2: Run latest version
    results.append("### Step 2 — Run Latest Version")
    memory = {}
    if MEMORY_FILE.exists():
        memory = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    proj_meta = memory.get("projects", {}).get(project, {})
    versions = proj_meta.get("versions", {})
    if versions:
        latest = sorted(versions.keys())[-1]
        try:
            code = run_version(project, latest)
            if code == 0:
                results.append(f"✅ Ran latest version ({latest}) successfully.\n")
            else:
                results.append(f"⚠️ Latest version ({latest}) exited with code {code}\n")
        except Exception as e:
            results.append(f"⚠️ Error running version {latest}: {e}\n")
    else:
        results.append("⚠️ No versions found.\n")

    # Step 3: Git status
    results.append("### Step 3 — Git Status")
    git_status = run_git(["status", "-sb"]) or "(git status failed)"
    results.append(f"```\n{git_status}\n```\n")

    return results


# ────────────────────────────────────────────────────────────────────────────────
# Chat Log Generator
def generate_chat_log(project, include_code=False, include_billy=False):
    """Generate a full to_chat_log.md for sharing here."""
    DOCS_DIR.mkdir(exist_ok=True)
    out_file = WORKSPACE / "to_chat_log.md"

    memory = {}
    if MEMORY_FILE.exists():
        memory = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))

    proj_meta = memory.get("projects", {}).get(project, {})
    versions = proj_meta.get("versions", {})

    lines = []
    lines.append(f"# To Chat Log — {project}")
    lines.append(f"Generated: {now_iso()}\n")
    lines.append(f"**Description:** {proj_meta.get('description','')}\n")
    lines.append(f"**Git enabled:** {proj_meta.get('git_enabled', False)}\n")
    lines.append(f"**Workspace:** {WORKSPACE}")
    lines.append(f"**Python:** {sys.version.split()[0]}\n")
    lines.append("---\n")

    # Repo status
    status = run_git(["status", "-sb"]) or "(git status failed)"
    commits = run_git(["log", "--oneline", "-5"]) or "(git log failed)"
    tags = run_git(["tag"]) or "(no tags)"
    lines.append("## Repo Status")
    lines.append(status + "\n")
    lines.append("## Recent Commits")
    lines.append(commits + "\n")
    lines.append("## Tags")
    lines.append(tags + "\n")
    lines.append("---\n")

    # Versions
    lines.append("## Versions")
    for v, meta in versions.items():
        lines.append(f"- {v}: {meta['description']} (created {meta['created_at']})")
        lines.append(f"  - file: {meta['filename']}")
        lines.append(f"  - copied_from: {meta.get('copied_from')}")
        lines.append(f"  - git_commit: {meta.get('git_commit')}")
        lines.append(f"  - last_run: {meta.get('last_run')}\n")

        if include_code:
            file_path = WORKSPACE / meta["filename"]
            if file_path.exists():
                try:
                    code = file_path.read_text(encoding="utf-8")
                    lines.append("```python")
                    lines.append(code.strip())
                    lines.append("```\n")
                except Exception as e:
                    lines.append(f"⚠️ Could not read {file_path}: {e}\n")

    # Project log
    log_file = DOCS_DIR / f"{project.upper()}_LOG.md"
    if log_file.exists():
        lines.append("## Project Log")
        lines.append(log_file.read_text(encoding="utf-8"))
    else:
        lines.append("## Project Log")
        lines.append("(no log yet)\n")

    lines.append("---\n")

    # Health checks
    lines.append("## Health Warnings")
    if not versions:
        lines.append("⚠️ No versions found.")
    else:
        missing = [v for v, m in versions.items() if not m.get("git_commit")]
        if missing:
            lines.append(f"⚠️ Versions missing commits: {', '.join(missing)}")
        else:
            lines.append("All versions have git commits ✅")
        latest = sorted(versions.keys())[-1]
        if versions[latest].get("last_run"):
            lines.append(f"- Latest version ({latest}) was run ✅")
        else:
            lines.append(f"- Latest version ({latest}) has not been run ⚠️")
    if log_file.exists():
        lines.append("- Project log present ✅")
    else:
        lines.append("- Project log missing ⚠️")

    # ────────────────────────────────────────────────
    # Test cycle results
    lines.append("\n---\n")
    lines.extend(run_test_cycle(project))

    # ────────────────────────────────────────────────
    # Billy’s own source snapshot
    if include_billy:
        lines.append("\n---\n")
        lines.append("## Billy Source Snapshot")
        billy_files = [WORKSPACE / "billy.py"] + sorted((WORKSPACE / "agent_billy").glob("*.py"))
        for bf in billy_files:
            if bf.exists():
                rel = bf.relative_to(WORKSPACE)
                lines.append(f"### {rel}")
                try:
                    code = bf.read_text(encoding="utf-8")
                    lines.append("```python")
                    lines.append(code.strip())
                    lines.append("```\n")
                except Exception as e:
                    lines.append(f"⚠️ Could not read {bf}: {e}\n")

    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"📄 To Chat Log generated at {out_file}")
    return 0
```

### agent_billy/cli.py
```python
# agent_billy/cli.py
import argparse
from . import core, git_ops, log, chatlog


def main():
    parser = argparse.ArgumentParser(
        prog="Agent Billy",
        description="Local Python-based project/version manager with Git integration."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Project ops
    p_create = sub.add_parser("create", help="Create a new project")
    p_create.add_argument("project")
    p_create.add_argument("-d", "--description", default="", help="Project description")
    p_create.add_argument("--git", action="store_true", help="Enable Git commits for this project")

    p_list = sub.add_parser("list", help="List projects or versions of a project")
    p_list.add_argument("project", nargs="?", help="Project name (optional)")

    p_save = sub.add_parser("save-version", help="Save a new version")
    p_save.add_argument("project")
    p_save.add_argument("version")
    p_save.add_argument("-m", "--message", default="", help="Description/commit message")
    p_save.add_argument("--from-version", default=None, help="Copy content from existing version")
    p_save.add_argument("--content", default=None, help="Inline content")

    p_run = sub.add_parser("run", help="Run a specific version")
    p_run.add_argument("project")
    p_run.add_argument("version")

    # Git passthrough
    p_git = sub.add_parser("git", help="Run raw git commands inside workspace")
    p_git.add_argument("git_args", nargs=argparse.REMAINDER)

    # Diff
    p_diff = sub.add_parser("diff", help="Show diff between two versions")
    p_diff.add_argument("project")
    p_diff.add_argument("version1")
    p_diff.add_argument("version2")

    # Log feature
    p_log = sub.add_parser("log", help="Append to project log (Recorder or Commit mode)")
    p_log.add_argument("project")
    p_log.add_argument("message", help="Log message (wrap in quotes)")
    p_log.add_argument("--commit", action="store_true", help="Also commit the log to Git")

    # Chat-log feature
    p_chatlog = sub.add_parser("chat-log", help="Generate to_chat_log.md for sharing here")
    p_chatlog.add_argument("project")
    p_chatlog.add_argument("--include-code", action="store_true", help="Include all project version source code")
    p_chatlog.add_argument("--include-billy", action="store_true", help="Include Billy's own source code")

    # Test-cycle feature
    p_test = sub.add_parser("test-cycle", help="Run automated sanity checks and log results")
    p_test.add_argument("project")

    args = parser.parse_args()

    # Dispatch
    if args.cmd == "create":
        return core.create_project(args.project, args.description, args.git)
    if args.cmd == "list":
        return core.list_projects(args.project)
    if args.cmd == "save-version":
        return core.add_version(args.project, args.version, args.message,
                                from_version=args.from_version, inline_content=args.content)
    if args.cmd == "run":
        return core.run_version(args.project, args.version)
    if args.cmd == "git":
        return git_ops.git_passthrough(args.git_args)
    if args.cmd == "diff":
        return core.diff_versions(args.project, args.version1, args.version2)
    if args.cmd == "log":
        return log.append_log(args.project, args.message, args.commit)
    if args.cmd == "chat-log":
        return chatlog.generate_chat_log(args.project,
                                         include_code=args.include_code,
                                         include_billy=args.include_billy)
    if args.cmd == "test-cycle":
        return chatlog.run_test_cycle(args.project)

    return 0
```

### agent_billy/core.py
```python
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
```

### agent_billy/git_ops.py
```python
from __future__ import annotations
import subprocess
from .utils import WORKSPACE

def run_git(args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=str(WORKSPACE),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"⚠️ git {' '.join(args)} failed:\n{e.stderr}")
        return None

def workspace_git_ready() -> bool:
    return (WORKSPACE / ".git").exists()

def ensure_workspace_git(verbose: bool = True) -> bool:
    if not workspace_git_ready():
        out = run_git(["init"])
        if verbose and out is not None:
            print("✅ Initialized git repository at workspace root.")
        return out is not None
    return True

def git_passthrough(args: list[str]) -> int:
    """Run a raw git command inside the workspace repo (used by CLI `git` subcommand)."""
    if not ensure_workspace_git(verbose=False):
        print("❌ No git repo in workspace.")
        return 1
    # passthrough: we don't capture output so interactive commands work
    result = subprocess.run(["git"] + args, cwd=str(WORKSPACE), text=True)
    return result.returncode
```

### agent_billy/log.py
```python
from __future__ import annotations
import os
from pathlib import Path
from datetime import datetime

from .utils import WORKSPACE, load_memory, save_memory
from .git_ops import run_git, ensure_workspace_git


def _logfile_for_project(project: str) -> Path:
    """Return the path to the project log file (docs/PROJECT_LOG.md)."""
    docs_dir = WORKSPACE / "docs"
    docs_dir.mkdir(exist_ok=True)
    return docs_dir / f"{project.upper()}_LOG.md"


def append_log(project: str, message: str, commit: bool = False) -> int:
    """
    Append a log entry for a project.
    
    If commit=True, also git-add and git-commit the log file.
    """
    memory = load_memory()
    if project not in memory["projects"]:
        print(f"❌ Project '{project}' not found in memory.json.")
        return 1

    log_path = _logfile_for_project(project)
    timestamp = datetime.now().isoformat(timespec="seconds")
    entry = f"- [{timestamp}] {message}\n"

    if not log_path.exists():
        header = f"# {project} Log\n\n"
        log_path.write_text(header + entry, encoding="utf-8")
    else:
        with log_path.open("a", encoding="utf-8") as f:
            f.write(entry)

    print(f"📝 Log updated: {log_path}")
    if commit:
        proj_meta = memory["projects"][project]
        if proj_meta.get("git_enabled") and ensure_workspace_git(verbose=False):
            run_git(["add", str(log_path)])
            run_git(["commit", "-m", f"{project} log: {message}"])
            print("✅ Log committed to Git.")
        else:
            print("⚠️ Git not enabled for this project, skipping commit.")

    return 0
```

### agent_billy/utils.py
```python
import json
from datetime import datetime
from pathlib import Path

# ────────────────────────────────────────────────────────────────────────────────
# Workspace constants
WORKSPACE = Path(__file__).resolve().parent.parent
PROJECTS_DIR = WORKSPACE / "projects"
MEMORY_FILE = WORKSPACE / "memory.json"

# ────────────────────────────────────────────────────────────────────────────────
# Helpers

def now_iso():
    """Return current time in ISO format (seconds precision)."""
    return datetime.now().isoformat(timespec="seconds")

def load_memory():
    """Load memory.json (project metadata)."""
    if not MEMORY_FILE.exists():
        return {"projects": {}}
    with MEMORY_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    """Save project metadata to memory.json."""
    with MEMORY_FILE.open("w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)
```
