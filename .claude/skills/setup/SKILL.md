---
name: setup
description: First-time setup for HW0, run once after cloning the fork. Checks the environment, adds the upstream remote, installs dependencies, checks the data loads, records the student's name and date, and commits. Run it again if anything breaks or to check a setup is complete.
---

Do these in order and show each command's output. Skip any that is already done. If a step
fails, say in plain words what the error means and what to change, and stop there.

1. `uname -sr` and `uv --version`.
   - If `uname` says Linux and the release contains `microsoft` or `WSL`, they are inside
     WSL2, which is where Windows students belong. If it says Windows, MINGW, MSYS or
     CYGWIN, they are in PowerShell or Git Bash: stop, and tell them to open the Ubuntu
     terminal and clone the repo again under their Ubuntu home, not under `/mnt/c`.
   - If `uv` is missing: `curl -LsSf https://astral.sh/uv/install.sh | sh`, then a new
     terminal. `INSTALL.md` has the rest.
2. `git remote -v`. If there is no `upstream`, add it:
   `git remote add upstream https://github.com/shilad/comp440-hw0`
3. `uv sync`
4. `uv run python run_all.py`. It should print `100,000 ratings, 1,682 movies, 943 users` and
   then three "unimplemented" lines.
5. Ask their name. Fill `**Name:**` and `**Date:**` at the top of `WRITEUP.md`. Those two are
   yours to type; nothing else in that file is.
6. `git add -A && git commit -m "Name and date"`. This picks up `uv.lock` if `uv sync`
   changed it.

Then say that setup is done and Part 1 is current: `human_part1.py`, on their own, with you
for installing and debugging only.
