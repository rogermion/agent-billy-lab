import argparse
from . import core, git_ops, log


def main():
    parser = argparse.ArgumentParser(
        prog="Agent Billy",
        description="Local Python-based project/version manager with Git integration."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # ── Project ops ───────────────────────────────────────────────────────────
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

    # ── Git passthrough ───────────────────────────────────────────────────────
    p_git = sub.add_parser("git", help="Run raw git commands inside workspace")
    p_git.add_argument("git_args", nargs=argparse.REMAINDER)

    # ── Diff ──────────────────────────────────────────────────────────────────
    p_diff = sub.add_parser("diff", help="Show diff between two versions")
    p_diff.add_argument("project")
    p_diff.add_argument("version1")
    p_diff.add_argument("version2")

    # ── Log feature ───────────────────────────────────────────────────────────
    p_log = sub.add_parser("log", help="Append to project log (Recorder or Commit mode)")
    p_log.add_argument("project")
    p_log.add_argument("message", help="Log message (wrap in quotes)")
    p_log.add_argument("--commit", action="store_true", help="Also commit the log to Git")

    args = parser.parse_args()

    # ── Dispatch ──────────────────────────────────────────────────────────────
    if args.cmd == "create":
        return core.create_project(args.project, args.description, args.git)
    if args.cmd == "list":
        return core.list_projects(args.project)
    if args.cmd == "save-version":
        return core.add_version(
            args.project,
            args.version,
            args.message,
            from_version=args.from_version,
            inline_content=args.content
        )
    if args.cmd == "run":
        return core.run_version(args.project, args.version)
    if args.cmd == "git":
        return git_ops.git_passthrough(args.git_args)
    if args.cmd == "diff":
        return core.diff_versions(args.project, args.version1, args.version2)
    if args.cmd == "log":
        return log.append_log(args.project, args.message, args.commit)

    return 0
