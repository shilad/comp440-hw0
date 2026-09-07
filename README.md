# COMP 440, HW0: Working With Data and Claude — Two Analysts, 100,000 Ratings

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
> `run_all.py` is the gate either way. The cold sessions run without tools (Claude writes code
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

## Purpose

Two analysts look at the same 100,000 ratings: you, alone, for 45 minutes, then Claude, cold,
with the identical questions. You build a table of where you disagree and who is right,
settled by evidence. Then two questions with no single right answer, which open HW1: the best
movie, and the most ___ movie. The grade is evidence that you can direct an AI, verify it, and
know when not to trust it. `CLAUDE.md` tells Claude how to behave in this repo; read it.
Every session leaves a trace: `TRANSCRIPT.md` for sessions here, `cold/` for cold ones.

## The data

MovieLens 100K (GroupLens Research, University of Minnesota; cite Harper and Konstan, 2015,
"The MovieLens Datasets: History and Context"): 100,000 ratings of 1–5 stars that 943
anonymous people gave 1,682 movies in 1997–98, every user with at least 20 ratings. `FILES.md`
describes the three files; `load_data.py` unzips the checked-in `ml-100k.zip` and loads them.
Before you count: nine titles carry accents, so reading `u.item` as UTF-8 fails
(`load_data.py` handles it), and 18 titles appear twice under different movie ids. The data
is public, so Claude may read it; your repo stays private, because the dataset may not be
redistributed. **[DECIDE: GroupLens (grouplens-info@cs.umn.edu) has not been asked for
classroom permission; the zip was rebuilt on Sep 5 from the canonical files because
files.grouplens.org served an expired certificate.]**

## How this repo works

- **Two commit messages you type yourself,** `Part 0 done` and `Part 1 finished`; everything
  else gets ordinary messages. Commit as you go; the history is part of the submission.
- **Claude may help with the code in Parts 2–4; the prose is yours.** Each script's docstring
  says what it must produce; each label in `WRITEUP.md` says what goes under it. `CLAUDE.md`
  states the rules; nothing enforces them. If Claude edits what it should not have, git has
  the old version; say so in `RECORD.md`.
- **`uv run python run_all.py`** runs every script in order from a clean slate.
- **`origin` is your own private copy,** never the template; the tools refuse otherwise. When
  I fix the template, Claude tells you at session start, and `uv run python sync_upstream.py`
  merges it without touching your files (a change to one of them waits as a patch under
  `tmp/upstream/`).

## The task

### Part 0. Setup (in class Thu Sep 10, plus up to 40 minutes at home)

Before class, install the tools and log in to Claude Code and GitHub: `INSTALL.md`. Then:

1. Make your own private copy of this template ("Use this template," private)
   **[DECIDE: or GitHub Classroom]** and clone it.
2. `uv sync`, then `uv run python load_data.py`.
3. `uv run python cold_session.py --selftest`.
4. In your editor, fill the five header lines of `WRITEUP.md`, then commit, yourself:
   `git add -A && git commit -m "Part 0 done"`.
5. Start `claude` here, trust the folder, and approve both hooks in `.claude/settings.json`.

In class, `uv run python cold_session.py warmup` asks a cold Claude how many ratings are
exactly 5 stars, and you check it with a one-liner. Also complete the Fall 2026 Background
Survey and join `#comp440-f26` on DevGarden Slack; both count under Part 5. Tell me by Fri
Sep 11 if anything does not install or log in.

### Part 1. You first (45 minutes, no Claude)

Set a timer, write the start time on the `**Timer started:**` line of `WRITEUP.md`, and close
`claude`. Answer the four questions in `part1.py` with your own pandas code, and explain each
answer in `WRITEUP.md`:

- (a) How many ratings, users, and movies are there, and how are ratings distributed across
  1–5 stars?
- (b) What is the median number of ratings per user, and how many users have 100 or more
  ratings?
- (c) Join ratings to titles. Which 10 movies have the most ratings?
- (d) Among movies with at least 20 ratings, which 10 have the highest mean rating? Show title,
  mean, and count.

No AI of any kind until the timer runs out, autocomplete included; documentation, Moodle's
pandas reference, and Slack (not for answers) are fine. An unfinished question gets a
`# STUCK (d): what I tried / where it broke` block in `part1.py` and the same note in
`WRITEUP.md`; stuck-notes earn credit, a blank does not, and `part1.py` must still run.

Then write `**Part 1 finished:** <date and time>` in `WRITEUP.md` and commit it yourself:

```
git add part1.py WRITEUP.md
git commit -m "Part 1 finished"
```

That commit is the marker: Part 1 is graded as it stood there, and Claude never edits
`part1.py` after it. A correction you make after seeing Claude's answers goes in the Part 2
stuck-questions line.

### Part 2. Claude second, then reconcile (about 75 minutes)

`uv run python cold_session.py part2` asks a fresh Claude outside this repo, given only the
file description in `FILES.md`, for one script answering the four questions, and commits the
capture (`cold/part2.md`, `cold/part2.jsonl`) and the script, unchanged, as
`part2_claude.py`. Run `uv run python part2_claude.py` as given; fix only import or path
errors, by hand, each marked with a `# Fix:` line at the top. Any other crash is a finding:
the rows it did not reach get the traceback's last line as Claude's answer.

Then the reconciliation table in `WRITEUP.md`: row 0 is the README's counts (100,000 / 943 /
1,682 / at least 20 ratings per user), rows (a)–(d) the questions. The verdict on Claude's
answer is HOLDS, FAILS, or CANNOT DETERMINE; a number never printed cannot hold or fail. Every
row, HOLDS included, names its evidence function in `part2_checks.py`, which says what makes a
function evidence. Every FAILS names a mechanism: *code bug*, *data trap*, *a different reading
of the spec*, *statistical misreading*, or *recalled rather than computed*. A wrong verdict
with sound evidence earns most of the row; a right one with none earns little.

For the **same method?** line, have Claude show the two scripts' loading, join, filter, and
grouping lines side by side; identical numbers from different code are a finding, not a
match. And the cold Claude has no data: every number in `cold/part2.md` and every constant in
`part2_claude.py` is from memory, whatever the prose says; computed means a script in this
repo printed it.

### Part 3. Two questions with no right answer (about 80 minutes: 30 for 3a, 30 for 3b, 20 for the cold sessions)

**3a. The best movie.** "What is the best movie in this dataset?" depends on how you combine
943 people's judgments. Choose a rule (`part3.py` lists the options), state it precisely on
the `**My rule:**` line of `WRITEUP.md`, and commit; until then `cold_session.py best` will
not run and Claude will not code it. Defend it in at most 150 words, and show the top 10 under
it and under an `**Alternative rule:**`.

**3b. The most ___ movie.** Pick an adjective, anything you can define. Nothing in the files
answers "Which movie is the *most* ___?" directly; you decide what it means, then compute it
(`part3.py` has a menu worked for *horror*; have Claude explain any term there that is new to
you before you choose). Write the adjective on the `**My adjective:**` line and a one-sentence
definition a classmate could code on the `**My definition:**` line; commit. Show the top 5
under it and under a `**Rival definition:**`, reflect in at most 150 words on what your
definition captures and misses, and say where "___-ness" lives in this dataset: the labels in
`u.item`, the crowd's behavior in `u.data`, or the text of the titles.

**Ask Claude cold, for both:** `uv run python cold_session.py best`, then
`uv run python cold_session.py most <your adjective>`. For each, a short paragraph: which rule
or definition Claude used, whether it said it was choosing, and whether its film came from
code you can run or from memory. Code with no film: run it in `part3.py` and report what it
crowns.

### Part 4. Your own question (about 45 minutes; Claude allowed for everything except the interpretation)

Ask one descriptive question about this collective of raters (`part4.py` has a menu, or bring
your own) and write it on the `**Question:**` line. `part4.py` says what it must produce: a
plot and a `check()` that prints MATCH or MISMATCH. Interpret the plot in at most 150 words of
your own, with at least one explicit limitation and one sentence on what evidence would change
your mind. If you use age, gender, or occupation: 943 people who used one website in 1997 are
not a sample of anyone, and I grade the honesty of the limitation, not the finding.

### Part 5. Collaboration record (about 30 minutes, written by you)

Fill every field of `RECORD.md`; Claude does not write there. Then ask Claude to review the
submission with you: it walks through what must be committed, filled in, and running, and
stops at the first thing missing. Commit, push, and prove the fresh clone runs:
`git clone <your repo url> hw0-check`, then `uv sync`, `uv run python load_data.py`, and
`uv run python run_all.py` inside it. Submit the repo URL (below).

One question to carry into HW1, which asks the same things of ten million ratings: what in your
scripts breaks when the table is a hundred times bigger?

## Required files and commit order

Yours: `WRITEUP.md`, `RECORD.md`, `part1.py`, `part2_checks.py`, `part3.py`, `part4.py`,
`figures/part4.png`. From `cold_session.py`, unchanged except `# Fix:` lines:
`cold/part2.md`, `cold/part2.jsonl`, `part2_claude.py`, `cold/best.md`,
`cold/most-<adjective>.md` (and `.jsonl`). From the Stop hook: `TRANSCRIPT.md`.

Commit order: `Part 0 done`, then `Part 1 finished`, then the Part 2 capture, then everything
else.

## Claude rules

**Required.** Claude's Part 2 and Part 3 answers come only from `cold_session.py`; `cold/` is
committed unedited; `part2_claude.py` runs as given, any fix marked `# Fix:`. Every number in
your prose comes from a named script or a capture you cite. A `# Claude:` comment sits above
any function Claude wrote (one line at the top if the whole file is).

**Prohibited.** Any AI in Part 1. Claude drafting, editing, or giving feedback on the graded
reasoning: verdicts and mechanisms, the defense, the definition and reflection, the
interpretation, the record. A number Claude recalled where a script should have computed it.
Train/test splits, error metrics, or recommender code: that is HW1. Sharing code, captures,
or transcripts with classmates in either direction (talking through approaches on Slack is
fine; name anyone who helped). A public repo.

## Claude collaboration record

`RECORD.md` has eight fields, listed in the file. It is the syllabus's account of AI
contributions, and later assignments ask for the same.

## Deliverables and how to submit

One private repo from this template, with every script running on a fresh clone. Submit the
repo URL via HW0 on Moodle **[DECIDE: Moodle assignment URL]** by **Thu Sep 17, 8:00am
Central**. The late-homework pass works as usual: once in the semester, up to three days, tell
me before the deadline.

## Rubric

| Criterion | Weight | Full credit looks like |
|---|---|---|
| **Part 1: You first** | 20 | Your own code, and it runs; correct answers, or (d) off by a defensible reading; specific stuck-notes; `part1.py` unchanged after the marker. |
| **Part 2: Claude second and reconciliation** | 25 | Every row has a verdict and an evidence function that computes rather than asserts; every FAILS a mechanism; a real same-method line. |
| **Part 3: Two questions with no right answer** | 25 | A rule and a definition precise enough to code; defense and reflection within 150 words, naming what is gained and lost; cold paragraphs that say which rule Claude used, whether it said so, and computed or recalled. |
| **Part 4: Your own question** | 15 | A plot that answers a one-sentence question; an interpretation within 150 words with a limitation and what would change your mind; a `check()` that matches or explains why not. |
| **Part 5: Record, setup, and repo hygiene** | 15 | Specific record fields; `TRANSCRIPT.md` and `cold/` unedited; every script runs on a fresh clone; commits in order; survey and Slack done. |
| | **100** | |

A record that says "checked, fine" with no method earns partial credit at most.

## If you would rather not use Claude (opt-out)

Opt out with no reason given and no grade effect: talk with me by Fri Sep 11. Your second
analyst is then my Reference Analyst pack, Claude's cold answers captured once by me;
`uv run python cold_session.py --import reference-analyst.zip` installs it.
**[DECIDE: the pack's "most ___" capture is for horror; either that is the adjective opt-out
students report on, or I run one capture per opt-out adjective on request.]** Everything else
is the same, rubric included; record field 2 becomes "what the Reference Analyst claimed," and
Part 4 is done without AI, `check()` included. The pack goes to the whole class at the Sep 17
debrief.

## If Claude (or something else) is down

A reported access problem never costs you points.

- `claude` is missing, or print mode is refused: `uv run python cold_session.py --interactive
  best` opens a cold session by hand and says how to save the capture (`--show-prompt` prints
  the prompt alone).
- Claude or your course account is down: post in `#comp440-f26` or email me, and use the
  Reference Analyst pack (`--import`) for Parts 2 and 3. An outage of more than about half a
  day extends the deadline by 48 hours **[DECIDE: 24 or 48]** without spending your late
  pass; so does a failure of your own account reported before the deadline.
- You declined the transcript hook: `uv run python dump_transcript.py` before committing.
- GitHub is down at the deadline: email me a zip of the repo without `data/`.
- Your laptop cannot run WSL2, `uv`, or Python 3.13: tell me by Fri Sep 11 **[DECIDE: lab
  machine, Codespace, or loaner]**.

## FAQ

**`cold_session.py` refuses to run.** It says why; usually a line in `WRITEUP.md` is empty or
not committed. To ask again, add `--again` and say in the record which capture you used.

**I mistyped the marker message.** `git commit --allow-empty -m "Part 1 finished"`, before you
ask Claude anything.

**Claude refused to pick my rule or adjective, or to look at Part 1 before the marker.**
Working as intended; choosing is the assignment.
