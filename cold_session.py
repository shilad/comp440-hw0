"""
The second analyst. Asks a cold Claude one of the assignment's questions and keeps the answer.

    uv run python cold_session.py warmup            # in class: how many ratings are exactly 5 stars?
    uv run python cold_session.py part2             # the four Part 1 questions, word for word
    uv run python cold_session.py best              # "What is the best movie in this dataset?"
    uv run python cold_session.py most horror       # "Which movie in this dataset is the most horror?"

"Cold" means: a fresh Claude Code session, started in an empty temporary directory outside
this repo, with no CLAUDE.md, no hooks, no tools, no data, and no memory of your work. It is
given the file description from FILES.md plus the question, and nothing else. Whatever it
says comes back verbatim into cold/<name>.md (readable) and cold/<name>.jsonl (the raw
event stream the readable file is rendered from), and the tool commits both. For `part2` it
also copies Claude's script, unchanged, into part2_claude.py, which you then run as given.

The tool refuses to run until the assignment says it is time:
  part2, best, most   need a commit whose message starts "Part 1 finished" (you go first);
  best                needs your own `**My rule:**` line committed in WRITEUP.md;
  most <adjective>    needs `**My adjective:** <adjective>` and `**My definition:**` committed.
A capture is never overwritten: to ask again, add --again (writes <name>-2.md, and so on)
and say in RECORD.md which capture you used.

Other commands:
    --show-prompt best | most horror | part2 | warmup   print the exact prompt (for a manual session)
    --interactive best ...                              open the cold session yourself and paste the prompt
    --selftest                                          prove the cold session ignores a CLAUDE.md and has no tools
    --import reference-analyst.zip                      install the instructor's Reference Analyst captures

Instructor-only flags (they are not hidden, just not for students): --captured-by instructor
skips the preconditions so the Reference Analyst pack can be made from a bare template, and
--with-tools runs the cold session with tools for experiments; captures say which was used.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path

# Windows consoles are not always UTF-8; never let a stray character crash a student's run.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

REPO = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO))
CLAUDE = shutil.which("claude") or "claude"  # on Windows the npm shim is claude.cmd; which() finds it
COLD = REPO / "cold"
FILES = REPO / "FILES.md"
PART2_FILE = REPO / "part2_claude.py"
# Pinned so every capture is comparable across students and days. HW0_COLD_MODEL and
# HW0_COLD_EFFORT override them (instructor experiments only).
MODEL = os.environ.get("HW0_COLD_MODEL", "claude-sonnet-5")
EFFORT = os.environ.get("HW0_COLD_EFFORT", "low")

QUESTIONS = {
    "warmup": "How many ratings in this dataset are exactly 5 stars?",
    "part2": (
        "Write Python (pandas) code that answers all four of these questions about the dataset, "
        "as one complete script.\n\n"
        "(a) How many ratings, users, and movies are there, and how are ratings distributed across 1–5 stars?\n"
        "(b) What is the median number of ratings per user, and how many users have 100 or more ratings?\n"
        "(c) Join ratings to titles. Which 10 movies have the most ratings?\n"
        "(d) Among movies with at least 20 ratings, which 10 have the highest mean rating? "
        "Show title, mean, and count."
    ),
    "best": "What is the best movie in this dataset?",
    "most": "Which movie in this dataset is the most {adj}?",
}
HEADER_TYPE = "hw0_capture_header"


# ---------------------------------------------------------------- helpers

def die(msg: str) -> None:
    print(msg)
    sys.exit(1)


def git(*args: str, check: bool = True) -> str:
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    if check and r.returncode != 0:
        die(f"git {' '.join(args)} failed:\n{r.stderr.strip()}")
    return r.stdout


def marker_commit() -> str | None:
    """Hash of the newest commit whose subject starts with 'Part 1 finished', or None."""
    r = subprocess.run(["git", "log", "--format=%H %s"], cwd=REPO, capture_output=True, text=True)
    for line in r.stdout.splitlines():
        h, _, s = line.partition(" ")
        if s.strip().lower().startswith("part 1 finished"):
            return h
    return None


def head_writeup_line(label: str) -> str | None:
    """The committed (HEAD) WRITEUP.md line that starts with **label:**, text after the label."""
    r = subprocess.run(["git", "show", "HEAD:WRITEUP.md"], cwd=REPO, capture_output=True, text=True)
    if r.returncode != 0:
        return None
    for line in r.stdout.splitlines():
        m = re.match(r"^\*\*" + re.escape(label) + r":\*\*\s*(.*)$", line.strip())
        if m:
            return m.group(1).strip() or None
    return None


def file_description() -> str:
    m = re.search(r"```\n(.*?)```", FILES.read_text(encoding="utf-8"), re.DOTALL)
    if not m:
        die("FILES.md has no fenced block.")
    return m.group(1).strip()


def build_prompt(kind: str, adj: str) -> str:
    q = QUESTIONS[kind].format(adj=adj) if kind == "most" else QUESTIONS[kind]
    return file_description() + "\n\n" + q


def norm_adj(adj: str) -> str:
    """Compare adjectives loosely: case, quotes, stray punctuation, and spacing do not matter."""
    return " ".join(re.sub(r"[^a-z0-9' ]+", " ", adj.lower()).replace("'", "").split())


def capture_name(kind: str, adj: str) -> str:
    if kind == "most":
        return "most-" + re.sub(r"[^a-z0-9]+", "-", norm_adj(adj)).strip("-")
    return kind


def next_free(name: str, again: bool) -> str:
    if not (COLD / f"{name}.md").exists():
        return name
    if not again:
        die(f"cold/{name}.md already exists. To ask again, add --again (the new capture is kept beside the "
            f"old one) and say in RECORD.md which one you used.")
    n = 2
    while (COLD / f"{name}-{n}.md").exists():
        n += 1
    return f"{name}-{n}"


def ancestor_claude_mds(start: Path) -> list[str]:
    found = []
    p = start.resolve()
    while True:
        if (p / "CLAUDE.md").exists():
            found.append(str(p / "CLAUDE.md"))
        if p.parent == p:
            return found
        p = p.parent


def claude_version() -> str:
    try:
        r = subprocess.run([CLAUDE, "--version"], capture_output=True, text=True)
    except FileNotFoundError:
        r = None
    if r is None or r.returncode != 0:
        die("Cannot run `claude --version`. Is Claude Code installed and on your PATH? "
            "See INSTALL.md.")
    return r.stdout.strip()


def cold_env() -> dict:
    env = dict(os.environ)
    for k in ("CLAUDECODE", "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_ENTRYPOINT"):
        env.pop(k, None)
    return env


def run_cold(prompt: str, cwd: Path, with_tools: bool = False) -> tuple[list[dict], list[str], str]:
    """Run one print-mode session. Returns (events, command, session_id)."""
    sid = str(uuid.uuid4())
    cmd = [CLAUDE, "-p", "--session-id", sid, "--no-session-persistence",
           "--setting-sources", "", "--output-format", "stream-json", "--verbose", "--max-turns", "30"]
    if with_tools:
        cmd += ["--permission-mode", "acceptEdits", "--allowedTools", "Bash", "Read", "Write", "Edit", "Glob", "Grep"]
    else:
        cmd += ["--tools", ""]
    if MODEL:
        cmd += ["--model", MODEL]
    if EFFORT:
        cmd += ["--effort", EFFORT]
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=cwd, env=cold_env())
    events = []
    for line in r.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    res = result_event(events)
    if r.returncode != 0 or not events or res.get("is_error"):
        why = str(res.get("result") or "").strip()
        die(f"claude -p failed (exit {r.returncode}). {why}\n{r.stderr.strip()[-1200:]}\n\n"
            f"If print mode is not available on your account, use --show-prompt and --interactive instead.")
    return events, cmd, sid


def reply_text(events: list[dict]) -> str:
    parts = []
    for e in events:
        if e.get("type") == "assistant":
            for b in e.get("message", {}).get("content", []):
                if b.get("type") == "text" and b.get("text", "").strip():
                    parts.append(b["text"].strip())
    return "\n\n".join(parts)


def tool_calls(events: list[dict]) -> list[dict]:
    out = []
    for e in events:
        if e.get("type") == "assistant":
            for b in e.get("message", {}).get("content", []):
                if b.get("type") == "tool_use":
                    out.append({"name": b.get("name"), "input": b.get("input")})
    return out


def result_event(events: list[dict]) -> dict:
    for e in events:
        if e.get("type") == "result":
            return e
    return {}


def render(header: dict, events: list[dict]) -> str:
    """The readable capture. A pure function of (header, events), so it can be re-rendered from the .jsonl."""
    res = result_event(events)
    calls = tool_calls(events)
    prompt = header["_prompt"]
    lines = ["# Cold session: " + header["name"], ""]
    for k, v in header.items():
        if not k.startswith("_"):
            lines.append(f"- {k}: {v}")
    lines += ["", "## What Claude was given (verbatim)", "", "```", prompt, "```", "",
              "## Claude's reply (verbatim)", ""]
    if calls:
        lines += ["Tool calls made in this session:", ""]
        lines += [f"- `{c['name']}` {json.dumps(c['input'])[:200]}" for c in calls]
        lines += [""]
    lines += [reply_text(events) or "(empty reply)", "", "## Session summary", "",
              f"- outcome: {res.get('subtype', '?')} · turns: {res.get('num_turns', '?')} · "
              f"cost_usd: {res.get('total_cost_usd', '?')}",
              f"- models: {', '.join((res.get('modelUsage') or {}).keys()) or 'n/a'}",
              f"- tool calls: {len(calls)}", ""]
    return "\n".join(lines)


def write_capture(name: str, header: dict, events: list[dict]) -> Path:
    COLD.mkdir(exist_ok=True)
    raw = COLD / f"{name}.jsonl"
    with open(raw, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"type": HEADER_TYPE, **header}) + "\n")
        for e in events:
            f.write(json.dumps(e) + "\n")
    md = COLD / f"{name}.md"
    md.write_text(rerender_from_jsonl(raw), encoding="utf-8", newline="\n")
    return md


def rerender_from_jsonl(raw: Path) -> str:
    """Rebuild the readable capture from the .jsonl alone; a grader can check it matches the .md."""
    text = raw.read_text(encoding="utf-8")  # universal newlines: the hash is the same on Windows
    lines = text.splitlines()
    header = json.loads(lines[0])
    if header.get("type") != HEADER_TYPE:
        raise ValueError(f"{raw} does not start with a capture header")
    header.pop("type")
    events = [json.loads(l) for l in lines[1:] if l.strip()]
    header["jsonl_sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return render(header, events)


def fences(reply: str) -> list[tuple[str, str]]:
    """Every fenced block in a reply as (info string, body), scanned line by line so a block
    with a different tag never swallows its neighbors."""
    out, info, body = [], None, []
    for line in reply.splitlines():
        if line.startswith("```"):
            if info is None:
                info, body = line[3:].strip().lower(), []
            else:
                out.append((info, "\n".join(body) + "\n"))
                info = None
        elif info is not None:
            body.append(line)
    return out


def code_blocks(reply: str) -> list[str]:
    """The Python code in a reply: fences tagged python/py, or, if there are none, untagged
    fences that compile as Python and look like code. Output and shell blocks are left out."""
    blocks = fences(reply)
    tagged = [b for info, b in blocks if info in ("python", "py", "python3")]
    if tagged:
        return tagged
    out = []
    looks_like_code = re.compile(r"^\s*(import\s|from\s+\w+\s+import|print\(|def\s|for\s|\w+\s*=[^=])", re.M)
    for info, b in blocks:
        if info:
            continue
        try:
            compile(b, "<reply>", "exec")
        except SyntaxError:
            continue
        if looks_like_code.search(b):
            out.append(b)
    return out


def extract_part2_code(reply: str, session_id: str, when: str) -> str:
    blocks = code_blocks(reply)
    head = (f"# Claude, unchanged. Extracted by cold_session.py from cold/part2.md "
            f"(session {session_id}, {when}).\n"
            f"# Fixes (import or path errors only), one per line, starting '# Fix:':\n\n")
    if not blocks:
        body = "\n".join("# " + l for l in reply.splitlines())
        return head + body + "\n\nraise SystemExit('Claude gave no code; see cold/part2.md')\n"
    return head + "\n\n".join(b.rstrip() + "\n" for b in blocks)


def commit_paths(paths: list[Path], message: str) -> None:
    rel = [p.relative_to(REPO).as_posix() for p in paths]
    name = git("config", "user.name", check=False).strip()
    email = git("config", "user.email", check=False).strip()
    if not name or not email:
        print("Files written but not committed: git does not know who you are yet. Run\n"
              "    git config --global user.name \"Your Name\"\n"
              "    git config --global user.email \"you@example.edu\"\n"
              f"then\n    git add {' '.join(rel)}\n    git commit -m \"{message}\"")
        return
    git("add", "--", *rel)
    git("commit", "-q", "-m", message, "--", *rel)
    print(f"Committed: {message}")


# ---------------------------------------------------------------- commands

def preconditions(kind: str, adj: str) -> dict:
    snap: dict = {}
    try:
        import sync_upstream
        problem = sync_upstream.origin_problem()
    except Exception:  # noqa: BLE001 - the origin check must not be the thing that breaks
        problem = None
    if problem:
        die("Repo check: " + problem)
    if kind == "warmup":
        return snap
    m = marker_commit()
    if not m:
        die("Part 1 is not committed yet: finish it yourself, then\n"
            "    git add part1.py WRITEUP.md && git commit -m \"Part 1 finished\"\n"
            "The second analyst goes second.")
    snap["part1_marker_commit"] = m[:12]
    if kind == "best":
        rule = head_writeup_line("My rule")
        if not rule:
            die("Write your rule on the `**My rule:**` line of WRITEUP.md and commit it, then ask Claude cold.\n"
                "You decide first.")
        snap["my_rule_at_head"] = rule
    if kind == "most":
        got = head_writeup_line("My adjective")
        definition = head_writeup_line("My definition")
        if not got or norm_adj(got) != norm_adj(adj):
            die(f"WRITEUP.md at HEAD says `**My adjective:** {got or ''}`; you asked for '{adj}'. "
                f"Write your adjective and definition on their lines, commit, then run this again.")
        if not definition:
            die("Write your one-sentence definition on the `**My definition:**` line of WRITEUP.md and commit it.")
        snap["my_adjective_at_head"] = got
        snap["my_definition_at_head"] = definition
    return snap


def do_capture(kind: str, adj: str, again: bool, captured_by: str, with_tools: bool) -> None:
    snap = preconditions(kind, adj) if captured_by == "student" else {}
    name = next_free(capture_name(kind, adj), again)
    prompt = build_prompt(kind, adj)
    print("=" * 72 + "\nPROMPT (this is all Claude gets):\n" + prompt + "\n" + "=" * 72)
    print("Asking Claude. This takes a minute or two, and nothing prints until it answers.")
    version = claude_version()
    tmp = Path(tempfile.mkdtemp(prefix="hw0-cold-"))
    try:
        ancestors = ancestor_claude_mds(tmp)
        events, cmd, sid = run_cold(prompt, tmp, with_tools)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    when = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    res = result_event(events)
    header = {
        "name": name,
        "captured_at": when,
        "captured_by": captured_by,
        "command": shlex.join(cmd[:2] + ["--session-id", "<id>"] + cmd[4:]),
        "cwd": "a fresh temporary directory outside the repo (deleted afterwards)",
        "claude_version": version,
        "models": ", ".join((res.get("modelUsage") or {}).keys()) or "n/a",
        "session_id": res.get("session_id", sid),
        "tools": "with tools (instructor experiment)" if with_tools else "none",
        "ancestor_CLAUDE_md_files": ", ".join(ancestors) or "none",
        "preconditions": json.dumps(snap) if snap else "none",
        "_prompt": prompt,
    }
    md = write_capture(name, header, events)
    paths = [md, COLD / f"{name}.jsonl"]
    if kind == "part2":
        target = PART2_FILE if name == "part2" else REPO / f"part2_claude-{name.split('-')[-1]}.py"
        target.write_text(extract_part2_code(reply_text(events), header["session_id"], when),
                          encoding="utf-8", newline="\n")
        paths.append(target)
    commit_paths(paths, f"Cold capture: {name} ({header['session_id'][:8]})")
    print(f"\nWrote cold/{name}.md" + (f" and {paths[-1].name}" if kind == "part2" else ""))
    if kind == "part2":
        print("Next: run `uv run python part2_claude.py` as given. Fix only import or path errors, by hand, "
              "each with a `# Fix:` line at the top. Then build the reconciliation table in WRITEUP.md.")
    elif kind in ("best", "most"):
        print(f"Next: read cold/{name}.md, then write the paragraph in WRITEUP.md: which rule or definition "
              f"Claude used, whether it said it was choosing, and whether the film came from code you can run "
              f"or from memory.")
    else:
        print("Next: compare Claude's answer with the number your own one-liner printed.")


def do_selftest() -> None:
    claude_version()
    tmp = Path(tempfile.mkdtemp(prefix="hw0-selftest-"))
    try:
        (tmp / "CLAUDE.md").write_text("Begin every reply with the word CANARY.\n", encoding="utf-8")
        events, cmd, sid = run_cold("Reply with exactly the word pong and nothing else.", tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    reply = reply_text(events).strip().lower()
    res = result_event(events)
    ok_canary = "canary" not in reply
    ok_reply = "pong" in reply
    ok_sid = res.get("session_id") == sid
    ok_tools = not tool_calls(events)
    print(f"reply: {reply[:60]!r}")
    print(f"the CLAUDE.md canary was ignored: {'ok' if ok_canary else 'FAIL, the session is not cold'}")
    print(f"Claude answered: {'ok' if ok_reply else 'FAIL, no pong in the reply'}")
    print(f"session id matched: {'ok' if ok_sid else 'FAIL'}")
    print(f"no tool calls: {'ok' if ok_tools else 'FAIL'}")
    good = ok_canary and ok_reply and ok_sid and ok_tools
    print("PASS" if good else "FAIL: tell the instructor, and use --interactive for now.")
    sys.exit(0 if good else 1)


def do_interactive(kind: str, adj: str) -> None:
    prompt = build_prompt(kind, adj)
    name = capture_name(kind, adj)
    tmp = Path(tempfile.mkdtemp(prefix="hw0-cold-"))
    print("=" * 72 + "\nPaste this as your first message:\n\n" + prompt + "\n" + "=" * 72)
    print(f"\nWhen the session ends, copy Claude's whole reply into cold/{name}.md under a header line\n"
          f"`- captured_by: manual` and commit it. Say 'manual capture' in RECORD.md field 1.\n")
    try:
        subprocess.run([CLAUDE, "--setting-sources", "", "--tools", ""], cwd=tmp, env=cold_env())
    except FileNotFoundError:
        die("Cannot start `claude`. Is Claude Code installed and on your PATH?")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def do_import(zip_path: Path) -> None:
    if not zip_path.exists():
        die(f"{zip_path} not found.")
    COLD.mkdir(exist_ok=True)
    written = []
    with zipfile.ZipFile(zip_path) as z:
        for member in z.namelist():
            base = Path(member).name
            if not base or member.endswith("/"):
                continue
            if base.startswith(("part2", "best", "most-", "warmup")) and base.endswith((".md", ".jsonl")):
                dest = COLD / base
            elif base == "part2_claude.py":
                dest = PART2_FILE
            else:
                continue
            if dest.exists():
                print(f"skip {dest.relative_to(REPO)}: already exists")
                continue
            dest.write_bytes(z.read(member))
            written.append(dest)
    if not written:
        die("Nothing imported (files already present, or the zip has no captures).")
    commit_paths(written, "Reference Analyst captures imported (instructor-run, unchanged)")
    print("Imported: " + ", ".join(str(p.relative_to(REPO)) for p in written))
    print("Say in RECORD.md field 1 that you used the Reference Analyst, and for which parts.")


def main(argv: list[str]) -> None:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    if "--selftest" in argv:
        do_selftest()
        return
    if "--import" in argv:
        i = argv.index("--import")
        if i + 1 >= len(argv):
            die("Give the zip: uv run python cold_session.py --import reference-analyst.zip")
        do_import(Path(argv[i + 1]))
        return
    captured_by = "student"
    if "--captured-by" in argv:
        i = argv.index("--captured-by")
        if i + 1 >= len(argv) or argv[i + 1] != "instructor":
            die("--captured-by takes exactly one value, instructor; students do not need it.")
        captured_by = "instructor"
        argv = argv[:i] + argv[i + 2:]
    flags = {a for a in argv if a.startswith("--")}
    args = [a for a in argv if not a.startswith("--")]
    if not args or args[0] not in QUESTIONS:
        die("Which question? warmup | part2 | best | most <adjective>   (see --help)")
    kind, adj = args[0], " ".join(args[1:]).strip()
    if kind == "most" and not adj:
        die("Give the adjective: uv run python cold_session.py most horror")
    if "--show-prompt" in flags:
        print(build_prompt(kind, adj))
        return
    if "--interactive" in flags:
        do_interactive(kind, adj)
        return
    do_capture(kind, adj, "--again" in flags, captured_by, "--with-tools" in flags)


if __name__ == "__main__":
    main(sys.argv[1:])
