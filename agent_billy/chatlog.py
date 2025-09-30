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
