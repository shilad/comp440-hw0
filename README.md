# COMP 440, HW0: Working With Data and Claude — An AI and Human Analyst

**Fall 2026 · Individual · 6% of the course grade**
**Out Thu Sep 10 · Due Thu Sep 17, 8:00am Central**

Budget about five and a half hours; aim to finish Parts 1–3 by Mon Sep 14. HW1 goes out Tue
Sep 15 and builds on this, so finish HW0 first.

> **Instructor notes (delete before publishing).** Decisions taken as defaults so the brief
> reads whole; each is one edit to change. Part 1(d) threshold and the shrinkage constant are
> both 20. The 45-minute timebox is guidance with attestation (timer lines in WRITEUP.md, the
> two commit timestamps, the hours field), not a hard rule. Any adjective is allowed in 3b. The
> outage extension is written as 48 hours and does not spend the late pass. Demographic columns
> are allowed in Part 4 with the limitation requirement. Weight (6%), due time (8:00am), the
> three-day late pass, and opt-out by talking with you follow the Sep 5 syllabus; the design doc
> and the earlier confirmation said 2%, 10:00am, and 48 hours, so switch back with one edit if
> HW0 is the exception. Grading is the rubric as written;
> `run_all.py` is the entry point, not a gate; Claude reviews the submission with the
> student. The cold sessions run without tools (Claude writes code
> it cannot run, you run it), which four trial captures on Sep 5 showed produces runnable
> scripts plus a recalled and false claim that titles are unique. Still marked `[DECIDE: ...]`
> below: the Claude account and the install page, the submission target, GroupLens's permission
> for the checked-in zip, the laptop fallback, the model pin for cold sessions, and whether HW1
> adopts `RECORD.md` (its repo currently ships DECISIONS.md and REFLECTION.md and uses ML-10M).
> Windows: WSL2 (Ubuntu) is required, per your Sep 5 decision, so Windows students run the
> exact Linux path tested here; native Windows, PowerShell, and Git Bash are unsupported. The
> install page must cover the WSL2 steps (Store install, reboot, virtualization enabled in
> firmware, Ubuntu username and password, VS Code WSL extension, repo under the Ubuntu home).
> Worth one dry run on a Windows laptop before Sep 10 anyway, mainly for the Claude Code login
> inside WSL2 on the course account type. The session-start hook fetches this template from
> GitHub each time `claude` starts (silent when offline), and `sync_upstream.py` merges fixes you
> push to the template's `main`; that only works if every student can read the template, so either
> keep it public, add the class as read-only collaborators, or use GitHub Classroom
> **[DECIDE]**. Push template fixes as ordinary commits; never rewrite the template's history
> after students have copied it. `TRANSCRIPT.md` is committed automatically after every session
> ("Auto-commit TRANSCRIPT.md"), so expect those commits in students' histories.

## Goals

* To refresh your knowledge of Python and data analysis.
* To get some basic hands-on practice with analyzing ratings data.
* To verify your Python and Claude environments are operating effectively.
* To gain some experience with the capabilities, limitations, and interactive experience with Claude.

## Overview:

You and Claude will independently look at the same 100,000 ratings and answer identical questions without help from each other. 
Afterward, wou will work together to compare your findings. 


In this assignment you will analyze the [MovieLens 100K](https://grouplens.org/datasets/movielens/100k/) dataset, which contains 100,000 ratings of 1–5 stars that 943
anonymous people gave 1,682 movies in 1997–98.  
`load_data.py` unzips the checked-in `ml-100k.zip` and reads them  into plain records, with a pandas conversion for each.
This work will feed into HW1, where you analyze a much larger and more complex dataset.


## How this repo works

- Two commit messages you type yourself: `Part 0 done` and `Part 1 finished`. Commit as you go,
  in this order: `Part 0 done`, then `Part 1 finished`, then the Part 2 capture, then everything else.
- Claude may help with the code in Parts 2–4; the prose is yours.
- `uv run python run_all.py` runs the whole assignment.
- Work in your own private copy, never the template. When I fix the template,
  `uv run python sync_upstream.py` merges the fix.
- Files you write: `WRITEUP.md`, `RECORD.md`, `part1.py`, `part2_checks.py`, `part3.py`, `part4.py`,
  `figures/part4.png`. Files the tools write, which you leave alone: `cold/`, `part2_claude.py`
  (except `# Fix:` lines), `TRANSCRIPT.md`.

## The task

### Part 0. Setup (in class Thu Sep 10)

Before class, follow `INSTALL.md`. Then:

1. Make your own private copy of this template ("Use this template," private) and clone it.
2. `uv sync`, then `uv run python load_data.py`.
3. `uv run python cold_session.py --selftest`.
4. Fill the five header lines of `WRITEUP.md` and commit: `git add -A && git commit -m "Part 0 done"`.
5. Start `claude` and approve the hooks.

In class we run `uv run python cold_session.py warmup` together. Also complete the Background
Survey and join `#comp440-f26` on Slack. Tell me by Fri Sep 11 if anything does not work.

### Part 1. You first (45 minutes, no Claude)

Set a timer, write the start time on the `**Timer started:**` line of `WRITEUP.md`, and close
`claude`. Answer the four questions in `part1.py` with your own code, and explain each answer
in `WRITEUP.md`:

- (a) How many ratings, users, and movies are there, and how are ratings distributed across
  1–5 stars?
- (b) What is the median number of ratings per user, and how many users have 100 or more
  ratings?
- (c) Join ratings to titles. Which 10 movies have the most ratings?
- (d) Among movies with at least 20 ratings, which 10 have the highest mean rating? Show title,
  mean, and count.

No AI of any kind until the timer runs out, autocomplete included. If you get stuck, leave a
`# STUCK (d): what I tried / where it broke` note in `part1.py` and in `WRITEUP.md`;
`part1.py` must still run.

Then write `**Part 1 finished:** <date and time>` in `WRITEUP.md` and commit:

```
git add part1.py WRITEUP.md
git commit -m "Part 1 finished"
```

Part 1 is graded as it stood at that commit.

### Part 2. Claude second, then reconcile (about 75 minutes)

`uv run python cold_session.py part2` asks a fresh Claude the same four questions and saves
its script as `part2_claude.py`. Run it as given; fix only import or path errors, each marked
with a `# Fix:` line.

Then fill the reconciliation table in `WRITEUP.md`. The verdict on each of Claude's answers is
HOLDS, FAILS, or CANNOT DETERMINE; a number never printed cannot hold or fail. Every row names
its evidence function in `part2_checks.py`. Every FAILS names a mechanism: *code bug*, *data
trap*, *a different reading of the spec*, *statistical misreading*, or *recalled rather than
computed*.

For the **same method?** line, have Claude show the two scripts' loading, join, filter, and
grouping lines side by side.

### Part 3. Two questions with no right answer (about 80 minutes)

**3a. The best movie.** Choose a rule (`part3.py` lists the options), state it on the
`**My rule:**` line of `WRITEUP.md`, and commit. Defend it in at most 150 words, and show the
top 10 under it and under an `**Alternative rule:**`.

**3b. The most ___ movie.** Pick an adjective, anything you can define, and decide what it
means (`part3.py` has a menu worked for *horror*). Write it on the `**My adjective:**` line and
a one-sentence definition a classmate could code on the `**My definition:**` line; commit. Show
the top 5 under it and under a `**Rival definition:**`, and reflect in at most 150 words on
what your definition captures and misses.

**Ask Claude cold, for both:** `uv run python cold_session.py best`, then
`uv run python cold_session.py most <your adjective>`. For each, write a short paragraph: which
rule or definition Claude used, whether it said it was choosing, and whether its film came from
code you can run or from memory.

### Part 4. Your own question (about 45 minutes)

Ask one descriptive question about these raters (`part4.py` has a menu, or bring your own) and
write it on the `**Question:**` line. Make the plot `part4.py` describes, and interpret it in
at most 150 words of your own, with at least one limitation and one sentence on what evidence
would change your mind.

### Part 5. Collaboration record and submission (about 30 minutes)

Fill every field of `RECORD.md`. Ask Claude to review the submission with you. Then commit,
push, and check that a fresh clone runs: `git clone <your repo url> hw0-check`, then `uv sync`
and `uv run python run_all.py` inside it. Submit the repo URL on Moodle by
**Thu Sep 17, 8:00am Central**.

One question to carry into HW1: what in your scripts breaks when the table is a hundred times
bigger?

## Claude rules

**Required.** Claude's Part 2 and Part 3 answers come only from `cold_session.py`; `cold/` is
committed unedited; `part2_claude.py` runs as given, any fix marked `# Fix:`. Every number in
your prose comes from a script you name. A `# Claude:` comment sits above any function Claude
wrote.

**Prohibited.** Any AI in Part 1. Claude drafting, editing, or giving feedback on the graded
reasoning: verdicts and mechanisms, the defense, the definition and reflection, the
interpretation, the record. Train/test splits, error metrics, or recommender code. Sharing
code, captures, or transcripts with classmates. A public repo.

## Rubric

| Criterion | Weight | Full credit |
|---|---|---|
| **Part 1: You first** | 20 | Your own code, and it runs; correct answers, or (d) off by a defensible reading; specific stuck-notes; `part1.py` unchanged after the marker. |
| **Part 2: Claude second and reconciliation** | 25 | Every row has a verdict and an evidence function; every FAILS a mechanism; a real same-method line. |
| **Part 3: Two questions with no right answer** | 25 | A rule and a definition precise enough to code; a defense and reflection within 150 words; cold paragraphs that say which rule Claude used and whether its film was computed or recalled. |
| **Part 4: Your own question** | 15 | A plot that answers your question; an interpretation within 150 words with a limitation; a `check()` that matches or explains why not. |
| **Part 5: Record, setup, and repo hygiene** | 15 | Specific record fields; `TRANSCRIPT.md` and `cold/` unedited; a fresh clone runs; commits in order; survey and Slack done. |
| | **100** | |

## If something is different

**You would rather not use Claude.** Talk with me by Fri Sep 11; there is no grade effect. You
then use my Reference Analyst pack as the second analyst:
`uv run python cold_session.py --import reference-analyst.zip`. Part 4 is done without AI.

**Claude, or something else, is down.** A reported access problem never costs you points.

- `claude` is missing or print mode is refused: `uv run python cold_session.py --interactive
  best` opens a cold session by hand.
- Claude or your course account is down: post in `#comp440-f26` or email me, and use the
  Reference Analyst pack for Parts 2 and 3. An outage of more than about half a day extends
  the deadline by 48 hours.
- You declined the transcript hook: run `uv run python dump_transcript.py` before committing.
- GitHub is down at the deadline: email me a zip of the repo without `data/`.
- Your laptop cannot run the tools: tell me by Fri Sep 11.

**`cold_session.py` refuses to run.** It says why; usually a line in `WRITEUP.md` is empty or
not committed. To ask again, add `--again` and say in the record which capture you used.

**You mistyped the marker message.** `git commit --allow-empty -m "Part 1 finished"`.

**Claude refused to pick your rule or adjective, or to look at Part 1 before the marker.**
Working as intended; choosing is the assignment.
