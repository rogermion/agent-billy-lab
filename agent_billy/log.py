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
