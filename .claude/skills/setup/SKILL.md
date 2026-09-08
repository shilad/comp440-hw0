---
name: setup
description: First-time setup for HW0, run once after cloning the fork. Checks the environment, adds the upstream remote, installs dependencies, checks the data loads, records the student's name and date, and commits. Run it again if anything breaks or to check a setup is complete.
---

Do these in order and show each command's output. Skip any that is already done. If a step
fails, say in plain words what the error means and what to change, and stop there.

1. `uname -sr`, and note whether it ran at all.
   - `Darwin` is macOS and `Linux` without more is Linux. Both are fine.
   - `Linux` with `microsoft` or `WSL` in the release is WSL2, where Windows students
     belong. Also check `pwd`: if the repo sits under `/mnt/c`, tell them to clone it
     again under their Ubuntu home, because it is slow and file watching does not work
     there.
   - `MINGW`, `MSYS` or `CYGWIN` means Git Bash. **Command not found** means PowerShell or
     cmd, which have no `uname`. Either way they are not in WSL2: stop, and tell them to
     install it from `INSTALL.md` and clone the repo again inside the Ubuntu terminal.
2. `uv --version`. If it is missing:
   `curl -LsSf https://astral.sh/uv/install.sh | sh`, then a new terminal. Nothing below
   works without it.
3. `git remote -v`. If there is no `upstream`, add it:
   `git remote add upstream https://github.com/shilad/comp440-hw0`
4. `uv sync`
5. `uv run python run_all.py`. It should print `100,000 ratings, 1,682 movies, 943 users` and
   then three "unimplemented" lines.
6. Ask their name. Fill `**Name:**` and `**Date:**` at the top of `WRITEUP.md`. Those two are
   yours to type; nothing else in that file is.
7. `git add -A && git commit -m "Name and date"`. This picks up `uv.lock` if `uv sync`
   changed it.

Then say that setup is done and Part 1 is current: `human_part1.py`, on their own, with you
for installing and debugging only.
