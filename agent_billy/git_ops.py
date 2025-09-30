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
