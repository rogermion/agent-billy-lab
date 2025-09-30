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
