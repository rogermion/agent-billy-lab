# Agent Billy Roadmap

This file tracks planned upgrades and long-term vision for Agent Billy.

---

## ✅ Current Status (v4)
- Project creation & versioning
- Auto-copy previous versions
- `memory.json` tracking
- Auto commits + Git tags per version
- Built-in `diff` command
- Git passthrough (push, pull, log, status)
- GitHub sync verified

---

## 🛠️ Next Steps (v5+)

### Short-term upgrades
- **checkout-version** → restore workspace to a tagged version
- **changelog generator** → auto-generate release notes from commit history
- **run logs** → capture stdout/stderr of each run
- **requirements tracking** → auto-generate/update `requirements.txt` from `--deps`

### Medium-term upgrades
- **project templates** → pre-seeded setups (Flask app, CLI tool, data script)
- **branching** → experimental branches (`dev`, `feature-X`) with merge support
- **configurable memory.json schema** → extra metadata (author, status, priority)
- **auto-testing hook** → run pytest/unittest before committing

### Long-term ideas
- **multi-agent support** → collaborate with other local agents
- **Docker integration** → auto-generate Dockerfiles
- **CI/CD hooks** → GitHub Actions templates on version save
- **web UI** → local dashboard for browsing projects/versions
