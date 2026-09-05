"""
Run every analysis script in order on a clean slate, then check the submission, the way the
grader will.

    uv run python run_all.py

This is the repo's version of "Runtime > Restart and run all": each script runs in its own
fresh Python process, in order, with a headless plotting backend; the first error stops the
run. Then CHECKS: commit order, frozen files, captures, anchors, word caps, record fields.
Exit code is non-zero on any FAIL. Do this from a fresh clone before you submit.
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
SCRIPTS = ["part1.py", "part2_claude.py", "part2_checks.py", "part3.py", "part4.py"]
# Re-asked captures (cold_session.py --again) produce part2_claude-2.py, -3.py ...; run them all.
SCRIPTS = SCRIPTS[:2] + sorted(p.name for p in Path(__file__).resolve().parent.glob("part2_claude-*.py")) + SCRIPTS[2:]
CAPPED = ["Defense", "Reflection", "Interpretation"]  # 150-word paragraphs in WRITEUP.md
ANCHORS = ["My rule", "Alternative rule", "My adjective", "My definition", "Rival definition", "Question"]
TQ, SQ = '"' * 3, "'" * 3  # triple quotes, for docstring detection

fails: list[str] = []
warns: list[str] = []


def ok(msg):
    print(f"  ok    {msg}")


def fail(msg):
    fails.append(msg)
    print(f"  FAIL  {msg}")


def warn(msg):
    warns.append(msg)
    print(f"  WARN  {msg}")


def git(*args):
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def run_scripts() -> int:
    env = dict(os.environ, MPLBACKEND="Agg")
    for name in SCRIPTS:
        path = REPO / name
        print(f"\n{'=' * 72}\n{name}\n{'=' * 72}")
        if not path.exists():
            print("(missing)")
            if name != "part1.py":
                fails.append(f"{name} is missing")
            continue
        r = subprocess.run([sys.executable, str(path)], cwd=REPO, env=env)
        if r.returncode != 0 and name.startswith("part2_claude"):
            # Claude's script is run as given; a crash is a finding for the table, not a fix.
            warn(f"part2_claude.py exited with code {r.returncode}. Per Part 2 that is a finding, not "
                 f"something to repair: the rows it did not reach get FAILS with the traceback as evidence.")
            continue
        if r.returncode != 0 and name == "part1.py":
            # Part 1 is graded as committed at the marker; do not edit it now, describe it instead.
            warn(f"part1.py exited with code {r.returncode}. Do not edit it now (Part 1 is graded as it was "
                 f"at the marker); describe what broke in the Stuck-notes line of WRITEUP.md.")
            continue
        if r.returncode != 0:
            print(f"\n{name} exited with code {r.returncode}. Fix it and run again.")
            return r.returncode
    return 0


def section(text: str, label: str) -> str:
    """Text after a bold **label...:** line up to the next bold label or heading."""
    m = re.search(r"^\*\*" + re.escape(label) + r"[^\n]*?:\*\*\s*(.*?)(?=^\*\*|^#|\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def anchor(text: str, label: str) -> str:
    """Text on the same line as **label:** (an empty line means the anchor is empty)."""
    m = re.search(r"^\*\*" + re.escape(label) + r":\*\*[ \t]*(.*)$", text, re.M)
    return (m.group(1) if m else "").strip()


def quoted_words(block: str) -> int:
    """Words in the blockquote lines of a section (the student's prose, not the tables)."""
    lines = [l[1:] for l in block.splitlines() if l.startswith(">")]
    return len(" ".join(lines).split())


def checks() -> None:
    print(f"\n{'=' * 72}\nCHECKS\n{'=' * 72}")
    log = [l.split(" ", 1) for l in git("log", "--reverse", "--format=%H %s").splitlines()]
    subj = {h: s.lower() for h, s in log}
    order = [h for h, _ in log]

    def first(pred):
        for h in order:
            if pred(h):
                return h
        return None

    p0 = first(lambda h: subj[h].startswith("part 0 done"))
    p1 = first(lambda h: subj[h].startswith("part 1 finished"))
    markers = [h for h in order if subj[h].startswith("part 1 finished")]
    # Part 1 is graded from the FIRST marker commit whose part1.py differs from the template's
    # stub: a marker that forgot `git add part1.py` is a slip, not a lost assignment, while a
    # later re-mark after editing never moves the line.
    stub_commit = order[0] if order else None
    p1_graded = next((h for h in markers if stub_commit and git("diff", stub_commit, h, "--", "part1.py").strip()), None)
    def touches(h, path):
        return path in git("show", "--name-only", "--format=", h)
    p2 = first(lambda h: touches(h, "cold/part2.md") or touches(h, "part2_claude.py"))
    p34 = first(lambda h: touches(h, "part3.py") or touches(h, "part4.py"))

    # 1. commit order
    if not p0:
        fail("no commit whose message starts 'Part 0 done'")
    if not p1:
        fail("no commit whose message starts 'Part 1 finished'")
    if p0 and p1 and order.index(p0) > order.index(p1):
        fail("'Part 0 done' comes after 'Part 1 finished'")
    if p1 and p2 and order.index(p2) < order.index(p1):
        fail("Claude's Part 2 code was committed before 'Part 1 finished'")
    if p2 and p34 and order.index(p34) < order.index(p2):
        fail("part3.py/part4.py were committed before the Part 2 capture")
    if p0 and p1 and order.index(p0) < order.index(p1) and (not p2 or order.index(p1) < order.index(p2)) \
            and (not p2 or not p34 or order.index(p2) < order.index(p34)):
        ok("commit order: Part 0 done, then Part 1 finished, then Part 2 capture")

    # 2. part1.py in the marker commit carries the student's own code (more than the stub)
    if p1 and p1_graded and p1_graded != p1:
        warn(f"the first 'Part 1 finished' commit ({p1[:8]}) did not include your part1.py; grading it from "
             f"{p1_graded[:8]} ({subj[p1_graded]})")
    if p1 and not p1_graded:
        fail("no 'Part 1 finished' commit contains your part1.py (only the stub): run `git add part1.py` and "
             "commit again with a message starting 'Part 1 finished'")
    if p1_graded:
        p1 = p1_graded
        print(f"  info  Part 1 graded from commit {p1[:8]}: {subj[p1]}")
        body = git("show", f"{p1}:part1.py")
        root = order[0] if order else None
        stub = git("show", f"{root}:part1.py") if root else ""

        def code_lines(text):
            out, in_doc = set(), False
            for line in text.splitlines():
                t = line.strip()
                if t.startswith(TQ) or t.startswith(SQ):
                    if (t.count(TQ) + t.count(SQ)) % 2 == 1:
                        in_doc = not in_doc
                    continue
                if in_doc or not t or t.startswith("#"):
                    continue
                out.add(t)
            return out

        own = code_lines(body) - code_lines(stub)
        if not body.strip():
            fail("part1.py is missing from the 'Part 1 finished' commit")
        elif len(own) < 3:
            fail("part1.py in the 'Part 1 finished' commit has no code beyond the stub")
        else:
            ok(f"part1.py in the 'Part 1 finished' commit has {len(own)} lines of the student's own code")
        if git("diff", p1, "HEAD", "--", "part1.py").strip():
            fail("part1.py changed after the 'Part 1 finished' commit (it is graded as committed there)")
        else:
            ok("part1.py unchanged since the marker")

    # 3. captures re-render
    cold = REPO / "cold"
    mds = sorted(cold.glob("*.md")) if cold.exists() else []
    if not mds:
        fail("no captures in cold/ (run cold_session.py part2, best, most <adjective>)")
    sys.path.insert(0, str(REPO))
    try:
        import cold_session
    except Exception as e:  # noqa: BLE001
        cold_session = None
        warn(f"cannot import cold_session.py ({e}); capture re-render skipped")
    for md in mds:
        raw = md.with_suffix(".jsonl")
        if not raw.exists():
            warn(f"{md.name}: manual capture (no .jsonl); the grader reads it as is")
            continue
        if cold_session is None:
            continue
        try:
            same = cold_session.rerender_from_jsonl(raw) == md.read_text(encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            same = False
            warn(f"{md.name}: could not re-render ({e})")
        if same:
            ok(f"{md.name} re-renders from its .jsonl unchanged")
        else:
            fail(f"{md.name} does not match its .jsonl: the capture was edited")
    for n in ("part2", "best"):
        if not (cold / f"{n}.md").exists():
            fail(f"cold/{n}.md missing")
    if not list(cold.glob("most-*.md")) if cold.exists() else True:
        fail("cold/most-<adjective>.md missing")

    # 4. each part2_claude*.py differs from its capture only by header and # Fix: lines
    pairs = [(REPO / "part2_claude.py", cold / "part2.md")]
    pairs += [(REPO / f"part2_claude-{m.stem.split('-')[-1]}.py", m) for m in sorted(cold.glob("part2-*.md"))] if cold.exists() else []
    if len(pairs) > 1:
        warn(f"{len(pairs)} Part 2 captures exist (cold_session.py --again); RECORD.md must say which one the table uses")
    for p2py, p2md in pairs:
        if p2py.exists() and p2md.exists():
            reply = p2md.read_text(encoding="utf-8").split("## Claude's reply (verbatim)", 1)[-1]
            blocks = cold_session.code_blocks(reply) if cold_session else []
            want = "\n\n".join(b.rstrip() + "\n" for b in blocks).strip().splitlines()
            have = [l for l in p2py.read_text(encoding="utf-8").splitlines()
                    if not l.startswith("# Claude, unchanged.") and not l.startswith("# Fixes (import or path")
                    and not l.startswith("# Fix:")]
            have = "\n".join(have).strip().splitlines()
            if want == have:
                ok(f"{p2py.name} matches the code in {p2md.relative_to(REPO).as_posix()}")
            else:
                fixes = [l for l in p2py.read_text(encoding="utf-8").splitlines() if l.startswith("# Fix:")]
                if fixes:
                    warn(f"{p2py.name} differs from its capture and declares {len(fixes)} fix line(s); "
                         f"the grader checks they are import or path fixes only")
                else:
                    fail(f"{p2py.name} differs from the code in its capture with no '# Fix:' line explaining why")
        elif p2py.exists() or p2md.exists():
            fail(f"{p2py.name} and {p2md.relative_to(REPO).as_posix()} must both exist")

    # 5-6. WRITEUP anchors and caps
    wu = (REPO / "WRITEUP.md").read_text(encoding="utf-8") if (REPO / "WRITEUP.md").exists() else ""
    for a in ANCHORS:
        if anchor(wu, a):
            ok(f"WRITEUP.md `**{a}:**` filled")
        else:
            fail(f"WRITEUP.md `**{a}:**` is empty")
    for a in ("Timer started", "Part 1 finished"):
        (ok if anchor(wu, a) else warn)(f"WRITEUP.md `**{a}:**` {'filled' if anchor(wu, a) else 'is empty'}")
    for label in CAPPED:
        words = quoted_words(section(wu, label))
        if words == 0:
            fail(f"WRITEUP.md `{label}` paragraph is empty")
        elif words > 150:
            warn(f"WRITEUP.md `{label}` is {words} words; the cap is 150 and graders stop there")
        else:
            ok(f"WRITEUP.md `{label}`: {words} words")

    # 7. RECORD fields
    rec = (REPO / "RECORD.md").read_text(encoding="utf-8") if (REPO / "RECORD.md").exists() else ""
    empties = re.findall(r"^- (.+?):\s*$", rec, re.M)
    if empties:
        fail("RECORD.md has empty fields: " + ", ".join(e.strip() for e in empties[:6]))
    else:
        ok("RECORD.md has no empty field lines")
    if re.search(r"^>\s*$", rec, re.M):
        warn("RECORD.md has an empty '>' answer block")

    # 8. figure
    if (REPO / "figures" / "part4.png").exists():
        ok("figures/part4.png exists")
    else:
        fail("figures/part4.png missing")

    # 9. origin and template
    try:
        import sync_upstream
        problem = sync_upstream.origin_problem()
        if problem:
            fail("repo: " + problem)
        else:
            ok("origin is your own repo, not the template")
            sync_upstream.ensure_upstream()
            if sync_upstream.fetch_upstream(timeout=20):
                ref = sync_upstream.upstream_ref()
                sync_upstream.graft_if_unrelated(ref)
                base, ahead, files = sync_upstream.status(ref)
                if ahead > 0:
                    warn(f"the template has {ahead} newer commit(s) ({', '.join(files[:5])}); "
                         f"run `uv run python sync_upstream.py`")
                elif ahead == 0:
                    ok("up to date with the template")
            else:
                warn("could not fetch the template (offline?); template updates not checked")
    except Exception as e:  # noqa: BLE001
        warn(f"template check skipped ({e})")

    # 10. transcript
    tr = REPO / "TRANSCRIPT.md"
    n_sessions = tr.read_text(encoding="utf-8").count("<!-- transcript-session:") if tr.exists() else 0
    if n_sessions:
        ok(f"TRANSCRIPT.md has {n_sessions} session(s)")
    elif mds:
        warn("TRANSCRIPT.md has no sessions; if you used Claude in this repo, run uv run python dump_transcript.py")
    else:
        warn("TRANSCRIPT.md missing")

    print(f"\n{len(fails)} FAIL, {len(warns)} WARN")


def main() -> int:
    rc = run_scripts()
    if rc:
        return rc
    print(f"\n{'=' * 72}\nScripts done." + ("" if warns else " All ran without error."))
    checks()
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
