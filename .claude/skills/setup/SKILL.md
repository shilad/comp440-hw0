---
name: setup
description: First-time setup for HW0, run once after cloning the fork. Checks the environment, adds the upstream remote, installs dependencies, checks the data loads, records the student's name and date, and commits. Run it again if anything breaks or to check a setup is complete.
---

Do these in order and show what you ran. Skip what is already done. If something fails, say
in plain words what it means and what to change, and stop there.

1. Make sure `git` and `uv` are installed, and if they are on Windows, that they have WSL2.
2. Add the `upstream` remote if it is missing:
   `git remote add upstream https://github.com/shilad/comp440-hw0`
3. `uv sync`, then `uv run python run_all.py`. It should print
   `100,000 ratings, 1,682 movies, 943 users` and three "unimplemented" lines.
4. Ask their name, and fill `**Name:**` and `**Date:**` at the top of `WRITEUP.md`. Those
   two are yours to type; nothing else in that file is.
5. Commit as `Name and date`.

Then say setup is done and Part 1 is current: `human_part1.py`, on their own, with you for
installing and debugging only.
