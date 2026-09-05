"""
Keep your repo honest and current with the assignment template.

    uv run python sync_upstream.py            # fetch the template and merge any fixes into your repo
    uv run python sync_upstream.py --check    # report only: is origin your own repo, is the template ahead

Two things this does:

1. Your work must live in your own repo (a fork or a copy of the template), never in the
   template itself. `origin` must not point at the template; load_data.py, cold_session.py,
   and run_all.py refuse when it does.

2. The template may get fixes during the week. This script adds the template as a remote
   named `upstream`, fetches it, and merges what changed. Template files (README.md,
   CLAUDE.md, the hooks, the tools, the data zip) take the template's version. Your files
   (part1.py, part2_claude.py, your scripts, WRITEUP.md, RECORD.md, cold/, figures/,
   TRANSCRIPT.md) are never overwritten: if the template changed one of them in a place you
   also changed, your version stays and the template's change is saved as a patch under
   tmp/upstream/ for you to apply by hand. Every merge is an ordinary merge commit, so
   `git log` shows exactly what came from the template and when.

A repo made with GitHub's "Use this template" does not share history with the template; the
script recognizes the template commit it was copied from and grafts the two histories
together (a local `git replace`, nothing rewritten) so ordinary merges work from then on.

Claude Code runs `--hook` at the start of every session (see .claude/settings.json); that only
reports, it never merges. Merge from a clean working tree: commit your work first.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

# Windows consoles are not always UTF-8; never let a stray character crash a student's run.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

REPO = Path(__file__).resolve().parent
UPSTREAM = os.environ.get("HW0_UPSTREAM", "https://github.com/shilad/comp440-hw0")
STUDENT_FILES = {"part1.py", "part2_claude.py", "part2_checks.py", "part3.py", "part4.py",
                 "WRITEUP.md", "RECORD.md", "TRANSCRIPT.md"}
STUDENT_DIRS = ("cold/", "figures/", "tmp/")


def git(*args: str, check: bool = True, timeout: int | None = None) -> str:
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def repo_key(url: str) -> str:
    """Normalize a remote URL to something comparable: owner/repo for GitHub, else the path."""
    u = url.strip()
    u = re.sub(r"\.git/?$", "", u)
    m = re.match(r"^(?:https?://|git@|ssh://git@)?(?:www\.)?github\.com[:/]+(.+)$", u, re.I)
    if m:
        return "github:" + m.group(1).strip("/").lower()
    p = Path(u.replace("file://", ""))
    try:
        return "path:" + str(p.resolve())
    except OSError:
        return "path:" + str(p)


def remotes() -> dict[str, str]:
    out = {}
    for line in git("remote", "-v", check=False).splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[-1] == "(fetch)":
            out[parts[0]] = parts[1]
    return out


def origin_problem() -> str | None:
    """None if origin is the student's own repo; otherwise a one-line explanation."""
    kind, msg = origin_state()
    return None if kind == "ok" else msg


def origin_state() -> tuple[str, str]:
    """('ok', url) | ('missing', why) | ('template', why)."""
    rem = remotes()
    if "origin" not in rem:
        return "missing", ("this repo has no `origin` remote. Create your own private repo (a fork or a "
                           "copy of the template), push to it, and make it `origin` before you submit.")
    if repo_key(rem["origin"]) == repo_key(UPSTREAM):
        return "template", (f"`origin` is the assignment template itself ({rem['origin']}). Work in your own "
                            f"private repo, never in the template: fork or copy it, clone that, and start "
                            f"again there.")
    return "ok", rem["origin"]


def ensure_upstream() -> None:
    rem = remotes()
    if "upstream" not in rem:
        git("remote", "add", "upstream", UPSTREAM)
    elif repo_key(rem["upstream"]) != repo_key(UPSTREAM):
        git("remote", "set-url", "upstream", UPSTREAM)


def fetch_upstream(timeout: int = 30) -> bool:
    try:
        git("fetch", "--quiet", "upstream", timeout=timeout)
        return True
    except (RuntimeError, subprocess.TimeoutExpired):
        return False


def upstream_ref() -> str:
    for b in ("main", "master"):
        if git("rev-parse", "--verify", "--quiet", f"upstream/{b}", check=False):
            return f"upstream/{b}"
    raise RuntimeError("the template has no main or master branch")


def root_commits() -> list[str]:
    return git("rev-list", "--max-parents=0", "HEAD").splitlines()


def graft_if_unrelated(ref: str) -> str | None:
    """A 'Use this template' copy has its own root commit whose tree equals some template commit's
    tree. Graft that root onto the matching template commit so merges have a common ancestor."""
    if git("merge-base", "HEAD", ref, check=False):
        return None
    for root in root_commits():
        tree = git("rev-parse", f"{root}^{{tree}}")
        for c in git("rev-list", ref).splitlines():
            if git("rev-parse", f"{c}^{{tree}}") == tree:
                git("replace", "--graft", root, c)
                return c[:8]
    return None


def status(ref: str) -> tuple[str | None, int, list[str]]:
    base = git("merge-base", "HEAD", ref, check=False) or None
    if base is None:
        return None, -1, []
    ahead = int(git("rev-list", "--count", f"{base}..{ref}") or 0)
    files = git("diff", "--name-only", base, ref).splitlines() if ahead else []
    return base, ahead, files


def is_student_file(path: str) -> bool:
    return path in STUDENT_FILES or path.startswith(STUDENT_DIRS)


def merge(ref: str, base: str | None) -> None:
    if git("status", "--porcelain", "--untracked-files=no"):
        sys.exit("Your working tree has uncommitted changes. Commit them first, then run this again.")
    args = ["merge", "--no-ff", "--no-commit", ref]
    if base is None:
        args.insert(1, "--allow-unrelated-histories")
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    conflicted = git("diff", "--name-only", "--diff-filter=U").splitlines()
    kept, taken, patches = [], [], []
    for f in conflicted:
        if is_student_file(f):
            git("checkout", "--ours", "--", f)
            kept.append(f)
            out = REPO / "tmp" / "upstream"
            out.mkdir(parents=True, exist_ok=True)
            patch = out / (f.replace("/", "__") + ".patch")
            diff = git("diff", base, ref, "--", f, check=False) if base else git("show", f"{ref}:{f}", check=False)
            patch.write_text(diff + "\n", encoding="utf-8")
            patches.append(patch.relative_to(REPO).as_posix())
        else:
            git("checkout", "--theirs", "--", f)
            taken.append(f)
        git("add", "--", f)
    if r.returncode != 0 and not conflicted:
        git("merge", "--abort", check=False)
        sys.exit(f"Merge failed:\n{r.stderr.strip()}")
    changed = git("diff", "--cached", "--name-only").splitlines()
    if not changed:
        git("merge", "--abort", check=False)
        print("Nothing to merge.")
        return
    msg = ["Merge template updates from upstream", ""]
    msg += [f"Updated from the template: {', '.join(c for c in changed if c not in kept) or 'nothing'}"]
    if taken:
        msg += [f"Template version taken where both sides changed: {', '.join(taken)}"]
    if kept:
        msg += [f"Kept your version (template change saved as a patch): {', '.join(kept)}"]
    git("commit", "-q", "-m", "\n".join(msg))
    print("Merged template updates:")
    for c in changed:
        print(f"  {'kept yours' if c in kept else 'updated'}  {c}")
    for p in patches:
        print(f"  The template also changed that file; its change is saved as {p}. Apply what applies by "
              f"hand (Claude can explain the patch; you make the edit).")
    if "ml-100k.zip" in changed:
        print("  The data zip changed: run `uv run python load_data.py` again after deleting data/.")
    if "FILES.md" in changed:
        print("  FILES.md changed. Captures you already made keep the prompt they were given (it is inside "
              "each capture); new captures use the new text.")


def report(hook: bool) -> int:
    problem = origin_problem()
    if problem:
        print(("Repo check: " if hook else "") + problem)
        if not hook:
            return 1
    try:
        ensure_upstream()
    except RuntimeError as e:
        print(f"Could not add the upstream remote: {e}")
        return 0 if hook else 1
    if not fetch_upstream(timeout=15 if hook else 30):
        if not hook:
            print("Could not reach the template on GitHub (offline, or not logged in). Try again later.")
            return 1
        return 0
    ref = upstream_ref()
    grafted = graft_if_unrelated(ref)
    base, ahead, files = status(ref)
    if base is None:
        print("This repo and the template share no history and no common snapshot; merge by hand or ask "
              "the instructor.")
        return 0 if hook else 1
    if ahead <= 0:
        if not hook:
            print("Template check: origin is your own repo; the template has no updates.")
        return 0
    print(f"Template update available: {ahead} commit(s) touching {', '.join(files[:8])}"
          f"{' ...' if len(files) > 8 else ''}. Run `uv run python sync_upstream.py` to merge"
          + (" (or ask Claude to)." if hook else "."))
    return 0


def main(argv: list[str]) -> int:
    if "--hook" in argv:
        try:
            return report(hook=True)
        except Exception as e:  # noqa: BLE001 - a session-start hook must never fail the session
            print(f"sync_upstream: skipped ({e})")
            return 0
    if "--check" in argv:
        return report(hook=False)
    problem = origin_problem()
    if problem:
        print(problem)
        return 1
    ensure_upstream()
    if not fetch_upstream():
        print("Could not reach the template on GitHub (offline, or not logged in). Try again later.")
        return 1
    ref = upstream_ref()
    grafted = graft_if_unrelated(ref)
    if grafted:
        print(f"Your repo was copied from template commit {grafted}; histories joined.")
    base, ahead, files = status(ref)
    if base is None:
        print("This repo and the template share no history and no common snapshot; merge by hand or ask "
              "the instructor.")
        return 1
    if ahead <= 0:
        print("Up to date with the template.")
        return 0
    print(f"The template has {ahead} new commit(s) touching: {', '.join(files)}")
    merge(ref, base)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
