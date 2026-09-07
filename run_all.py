"""
Run every analysis script in order, each in its own fresh Python process.

    uv run python run_all.py

This is the repo's version of "Runtime > Restart and run all": nothing carries over from one
script to the next, and plots draw to files rather than windows. A missing script is noted and
skipped. part1.py and part2_claude.py run as they are; if either crashes, that is described in
WRITEUP.md, not repaired here. Any other crash stops the run and is yours to fix. Run this from
a fresh clone before you submit.
"""

from __future__ import annotations

import os
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
SCRIPTS = SCRIPTS[:2] + sorted(p.name for p in REPO.glob("part2_claude-*.py")) + SCRIPTS[2:]


def main() -> int:
    env = dict(os.environ, MPLBACKEND="Agg")
    notes: list[str] = []
    for name in SCRIPTS:
        path = REPO / name
        print(f"\n{'=' * 72}\n{name}\n{'=' * 72}")
        if not path.exists():
            print("(missing)")
            notes.append(f"{name} is missing")
            continue
        r = subprocess.run([sys.executable, str(path)], cwd=REPO, env=env)
        if r.returncode == 0:
            continue
        if name.startswith("part2_claude"):
            # Claude's script runs as given; a crash is a finding for the table, not a fix.
            notes.append(f"{name} exited with code {r.returncode}: a finding for the reconciliation "
                         f"table, not something to repair")
            continue
        if name == "part1.py":
            # Part 1 is graded as committed at the marker; describe the crash, do not edit the file.
            notes.append(f"part1.py exited with code {r.returncode}: say what broke in the stuck-notes; "
                         f"do not edit it now")
            continue
        print(f"\n{name} exited with code {r.returncode}. Fix it and run again.")
        return r.returncode
    print(f"\n{'=' * 72}\nAll scripts ran.")
    for note in notes:
        print(f"  note  {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
