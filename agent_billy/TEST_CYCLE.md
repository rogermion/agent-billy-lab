# Agent Billy — Test Cycle

This checklist validates that Billy is working correctly after changes.

---

## ✅ Quick Sanity Checks
- [ ] `python3 billy.py -h` shows CLI help
- [ ] `python3 billy.py list` shows existing projects
- [ ] `python3 billy.py run <project> <latest_version>` executes without error
- [ ] `python3 billy.py log <project> "test log"` appends entry
- [ ] `python3 billy.py git status` runs and returns
- [ ] `python3 billy.py diff <project> <vX> <vY>` works when commits exist

---

## ⚙️ Extended Checks
- [ ] Git push/pull works (if remote configured)
- [ ] Chat-log generation (`--include-billy`) includes all source
- [ ] Memory.json updated correctly after new version
