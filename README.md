# COMP 440, HW0: Working With Data and Claude — Two Analysts, 100,000 Ratings

**Fall 2026 · Individual · 6% of the course grade**
**Out Thu Sep 10 · Due Thu Sep 17, 8:00am Central**

Budget about five and a half hours. HW1 goes out Tue Sep 15, before this is due; nothing in
HW1 is due before HW0, and HW1 uses the same tooling (uv, git, Claude Code, the transcript
hook) on a MovieLens a hundred times bigger, so finish HW0 first. Aim to have Parts 1–3 done by Mon Sep 14.

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

This assignment gets you set up with the tools we use all semester (Python and uv, git and
GitHub, Claude Code, Slack, Moodle) and introduces the working pattern every later assignment
assumes: you decide, Claude drafts, you check, you explain, you document. Two analysts will
look at the same 100,000 movie ratings: you and Claude. You go first, on your own, for 45
minutes. Then Claude gets the identical questions cold, and you build a table of where the two
of you disagree and who is right, settled by evidence from the data rather than by trusting
either of you. Two questions have no single right answer. "What is the best movie in this
dataset?" depends on how you combine many people's judgments. "What is the most ___ movie?"
(you fill in the blank: most horror, most romantic, most 90s, most cult) depends on what you
decide the word means and where you look for it: in the labels someone attached, in what the
crowd actually did, or in the words of the titles. Those are the first big ideas of this course
and the opening problems of HW1. The point of HW0 is not a polished analysis. It is evidence
that you can direct an AI, verify it, and know when not to trust it, on the kind of data you
will use again next week. If your Python is rusty, Part 1 is your refresher; if it is not, Part 1 will
take you twenty minutes.

This repo's `CLAUDE.md` tells Claude how to behave here. Read it; it is a description of how
you will direct the tool, not a restriction. Everything you do with Claude leaves a trace:
sessions in this folder are logged to `TRANSCRIPT.md`, and the cold sessions are captured
into `cold/`.

## The data

MovieLens 100K, from GroupLens Research at the University of Minnesota: 100,000 ratings (1–5
stars) that 943 people gave 1,682 movies on the MovieLens site between September 1997 and
April 1998. Three files: `u.data` (user, movie, rating, timestamp; tab-separated), `u.item`
(movie id, title, release date, an always-empty video release date, IMDb URL, 19 genre flags;
pipe-separated, latin-1 encoded), and `u.user` (user id, age, gender, occupation, zip;
pipe-separated). Users are anonymous integers. The dataset is public and released for research
and teaching (cite Harper and Konstan, 2015, "The MovieLens Datasets: History and Context").
The README inside the zip is our ground truth: 100,000 ratings, 943 users, 1,682 movies, every
user with at least 20 ratings. Because the data is public and anonymized, Claude may read it,
here or in the cold sessions. Two things worth knowing before you count anything: nine titles
carry accented characters, so reading `u.item` as UTF-8 fails (`load_data.py` handles it), and
18 titles appear twice under different movie ids.

The zip ships with this repo (`ml-100k.zip`), so setup never depends on GroupLens being
reachable; `uv run python load_data.py` unzips it into `data/`. Keep your repo private: the
dataset's README asks that it not be redistributed without permission. **[DECIDE: GroupLens
(grouplens-info@cs.umn.edu) has not been asked for classroom permission; the zip was rebuilt on
Sep 5 from the canonical files because files.grouplens.org served an expired certificate.]**

## How this repo works

- **Files you write:** `part1.py`, `part2_checks.py`, `part3.py`, `part4.py`, `WRITEUP.md`,
  `RECORD.md`. Claude may help with the code in Parts 2–4; the prose is yours.
- **Files the tools write:** `cold/` and `part2_claude.py` (by `cold_session.py`), `figures/`
  (by your scripts), `TRANSCRIPT.md` (by a hook, every time a Claude Code session in this folder
  ends; the hook also commits it by itself, so the record is always in your history). You
  never edit `cold/` or `TRANSCRIPT.md`; `part2_claude.py` stays unchanged except for import
  or path fixes, each announced by a `# Fix:` line at the top.
- **Two commit messages you type yourself:** `Part 0 done` and `Part 1 finished`. Everything
  after that gets ordinary messages. Commit as you go; your history is part of the submission.
- **`uv run python run_all.py`** runs every script from a clean slate and checks the
  submission. It is the first thing the grader runs.
- **Your repo, not the template.** Everything happens in your own private copy of this
  template; `origin` must be your repo. `load_data.py` refuses to run in the template itself,
  and `cold_session.py` and `run_all.py` refuse without your own `origin`.
- **Template fixes.** If I fix something in the template during the week, Claude tells you at
  the start of your next session (a hook fetches the template's `upstream` remote), and
  `uv run python sync_upstream.py` merges the fix as an ordinary merge commit. Template files
  take the template's version; your files are never overwritten. If the template changed a
  file that is yours (say, a label in `WRITEUP.md`), your version stays and the change lands
  as a patch under `tmp/upstream/` for you to apply by hand.
- **Work in this directory.** Sessions started elsewhere are not captured. The cold sessions
  are the one exception, and `cold_session.py` handles them.
- **The Claude rules are not enforced by a program**; `CLAUDE.md` states them and Claude
  follows them. Read it — there is nothing hidden. What checks after the fact is `run_all.py`:
  it fails if `part1.py` changed since the marker commit, or if `part2_claude.py` or a capture
  in `cold/` no longer matches what the cold session produced. If Claude edits something it
  should not have, git still has the old version; say what happened in `RECORD.md`.

## The task

### Part 0. Setup (in class Thu Sep 10, plus up to 40 minutes at home)

**Windows: this assignment runs inside WSL2, not in PowerShell, cmd, or Git Bash.** Install
WSL2 with Ubuntu (Microsoft Store, then reboot), then do every install and every command in
this brief inside the Ubuntu terminal, and keep your repo in the Linux filesystem (under your
Ubuntu home folder, not under `/mnt/c/...`). Edit files with VS Code and its WSL extension,
which opens the folder inside Ubuntu. The tools, the hooks, and the cold sessions were tested
on Linux; WSL2 is that same environment. On a Mac, Terminal is fine as it is.

Before class, following the page on Moodle **[DECIDE: install-and-login page, posted by Mon
Sep 8, including the WSL2 steps; which Claude account students use]**: install `uv`, `git`,
Claude Code, and VS Code (with the WSL extension on Windows; turn off any AI autocomplete in it
for Part 1); log in to Claude Code, and log in to GitHub from the terminal so that a private
repo can be cloned and pushed (`gh auth login`, or the method on the install page). Then:

1. Create your private repo from this template **[DECIDE: GitHub Classroom link, or "Use this
   template" as a private repo and add the instructor's GitHub handle as collaborator]** and
   `git clone` it. If git does not know you yet:

   ```
   git config --global user.name "Your Name"
   git config --global user.email "you@macalester.edu"
   ```

2. `uv sync`, then `uv run python load_data.py`. Expect the README, four `OK` lines, and a
   "Repo check" line naming your own repo as `origin`.
3. `uv run python cold_session.py --selftest`. Expect `PASS`. This proves the cold sessions
   really are cold on your machine.
4. In your editor, not in Claude, fill the five header lines of `WRITEUP.md` (title, name,
   HW0, date, and either "Using Claude" or "Opt-out path"). Claude will not open `WRITEUP.md`
   until Part 1 is done, so the header is yours to type. Then, yourself:

   ```
   git add -A
   git commit -m "Part 0 done"
   ```

5. Start `claude` in the repo. It first asks you to trust the folder and to approve the two
   hooks from `.claude/settings.json` (one checks your repo at the start of a session, the
   other writes `TRANSCRIPT.md` at the end); say yes to both. Type `hello`; it should run
   `git log`, see your commit, and tell you Part 1 is next.

In class we run `uv run python cold_session.py warmup` together: it asks a cold Claude how many
ratings are exactly 5 stars, and you check it against a one-liner of your own. If you have not
already, complete the Fall 2026 Background Survey and join `#comp440-f26` on DevGarden Slack.
Tell me by Fri Sep 11 if anything does not install or log in; a reported access problem never
costs you points.

### Part 1. You first (45 minutes, no Claude)

Set a timer and write the start time on the `**Timer started:**` line of `WRITEUP.md`. Close
your `claude` session. With your own pandas code in `part1.py`, and one sentence of explanation
per answer in `WRITEUP.md`, answer:

- (a) How many ratings, users, and movies are there, and how are ratings distributed across
  1–5 stars?
- (b) What is the median number of ratings per user, and how many users have 100 or more
  ratings?
- (c) Join ratings to titles. Which 10 movies have the most ratings?
- (d) Among movies with at least 20 ratings, which 10 have the highest mean rating? Show title,
  mean, and count.

You may use the pandas reference on Moodle, the "Intro to Python Notebooks" notebook, and Slack
for questions that are not "what is the answer." No AI of any kind until the timer runs out,
including "just check my code." Claude in this repo will refuse anyway. If a question is
unfinished when the timer ends, leave what you have in a comment block under a
`# STUCK (d): what I tried / where it broke` line, and write the same stuck-note in
`WRITEUP.md`. Stuck-notes earn credit; a blank does not. `part1.py` must still run.

Then write `**Part 1 finished:** <date and time>` in `WRITEUP.md` and commit it yourself:

```
git add part1.py WRITEUP.md
git commit -m "Part 1 finished"
```

That commit is the marker. Claude will not touch Part 1 before it exists, and
`cold_session.py` will not run. After it, you may ask Claude to explain pandas concepts and
error messages, and it may read your `part1.py`; it will never edit it, because Part 1 is
graded as it was at that commit. The same goes for your Part 1 answers and stuck-notes in
`WRITEUP.md`: they are graded as they stood at the marker, and a correction you make after
seeing Claude's answers goes in the Part 2 stuck-questions line, not into the Part 1 answer.
Two repairs, both before you ask Claude anything: if you
mistyped the message, `git commit --allow-empty -m "Part 1 finished"`; if you forgot
`git add part1.py`, add it and commit again with the same message (Part 1 is graded from the
first marker commit that contains it). If `part1.py` turns out not to run, do not fix it after
the marker; say what broke in the stuck-notes, and `run_all.py` will report the crash and carry
on.

### Part 2. Claude second, then reconcile (about 75 minutes)

Run `uv run python cold_session.py part2`. It starts a fresh Claude outside this repo with the
file description from `FILES.md` and the four questions, word for word, wrapped in one sentence
asking for a single script (`--show-prompt part2` prints it), and nothing else: no `CLAUDE.md`,
no tools, no data, no memory of your work. It saves the whole exchange as `cold/part2.md` (plus
`cold/part2.jsonl`, the raw event stream that `run_all.py` re-renders the readable file from),
copies Claude's script unchanged to `part2_claude.py`, and commits all three.

Run `uv run python part2_claude.py` as given. Fix only import or path errors, by hand, each
with a `# Fix:` line at the top of the file, and say so in `WRITEUP.md`. If it crashes for any
other reason, do not fix it: for the rows it did not reach, Claude's answer is the last line of
the traceback, the verdict is FAILS with the mechanism you diagnose (an encoding crash is a
data trap), and the evidence is the traceback plus your own check; `run_all.py` reports the
crash and carries on. You may ask Claude in the repo to explain the error, and to walk you
through what its cold script does line by line; the check and the words in the table are yours.

Now build the reconciliation table in `WRITEUP.md`, one row per item, with these columns:
*question · mine · Claude's · match? · verdict on Claude's answer · mechanism if it fails ·
evidence (`part2_checks.py::function`)*.

- **Row 0 is the README.** Both your counts and Claude's have to match 100,000 / 943 / 1,682 /
  at least 20 ratings per user. Your side is what `load_data.py` printed, recomputed by a
  function in `part2_checks.py`; Claude's side is what `part2_claude.py` printed for (a), with
  "not printed" for any number it did not print. A number that was never printed cannot hold
  or fail, which is what the CANNOT DETERMINE verdict is for; the verdict cell is still yours.
  If either side does not match, that is your first divergence to run down.
- **Rows (a)–(d)** are the four questions. A verdict is **HOLDS**, **FAILS**, or **CANNOT
  DETERMINE**. **Every row, HOLDS included, names a function in `part2_checks.py` that
  computes its deciding evidence**; a HOLDS with no evidence function is not yet a verdict,
  because two scripts can print the same numbers from different code. Every FAILS also needs
  a named mechanism: *code bug*; *data trap* (duplicate titles in `u.item`, an encoding, a
  silent NaN); *a different reading of the spec* (what "at least 20" means, how ties break,
  whether "movie" means a title or an id); *statistical misreading*; or *recalled rather than
  computed*. A wrong verdict backed by a sound evidence function earns most of the credit for
  that row. A right verdict with no evidence earns little.
- **Same method?** Under the table, one or two sentences on whether the two scripts computed
  the answers the same way (the join key, the filter, how ties break, whether "movie" meant a
  title or an id), naming one difference you found or what you compared to conclude there is
  none. Ask Claude to put the two scripts' loading, join, filter, and grouping lines next to
  each other first; spotting the difference is yours, and you answer from the code, not from
  the printed numbers. Identical numbers from different code are a finding, not a match.
- Where Part 1 has a stuck-note, Claude's version is your worked example: explain in your own
  words what its code does, then confirm it with a check.
- Name **one thing Claude said that you could not verify**, and why. If there is genuinely
  nothing, say what you checked to conclude that.

Claude in this repo may compute any check you specify and explain any code, including
`part2_claude.py` and your own `part1.py`; the verdicts and mechanisms are yours, and it will
not offer them.

One warning. Claude has seen this dataset many times. The cold Claude has no tools and no data,
so every number, film name, and claim in `cold/part2.md` is from memory, whatever the prose
says; a number typed into `part2_claude.py` as a constant is from memory too. A number is
computed only if a script in this repo printed it. Inside this repo, `CLAUDE.md` tells Claude
not to quote from memory; watch for it anyway. If Claude gave you a number no script produced,
it goes in the table as FAILS with mechanism "recalled rather than computed," or in the record
as something you could not verify.

### Part 3. Two questions with no right answer (about 80 minutes: 30 for 3a, 30 for 3b, 20 for the cold sessions)

**3a. The best movie** (about 30 minutes). "What is the best movie in this dataset?" has no
single answer, because it depends on how you combine 943 people's judgments. Choose a rule and
state it precisely: the plain mean; the mean among movies with at least N ratings; the number
of ratings; or a shrunk mean, `score = (n * mean + k * global_mean) / (n + k)` with a `k` you
choose and defend (the assignment recommends no k; say what a larger or a smaller k would do).
Write it on the `**My rule:**` line of `WRITEUP.md` and commit before you ask Claude to code
`part3.py`; `cold_session.py best` will not run until that line is committed. Defend your rule
in at most 150 words, naming one thing it gains and one thing it loses. Show the top 10 under
your rule and under one other rule, and write two or three sentences on which films moved and
why. (Optional: a scatter of mean against count makes the trade-off visible.)

**3b. The most ___ movie** (about 30 minutes). Now pick an adjective and ask "Which movie in
this dataset is the *most* ___?" Most horror. Most romantic. Most 90s. Most cult. Most family.
Most divisive. Anything you can define. Nothing in the files answers such a question directly.
`u.item` has genre flags, but 1 or 0 is not "more" or "less," and a film flagged
Horror|Comedy|Romance is arguably less horror than one flagged Horror alone; for an adjective
like "cult" or "90s" there is no flag at all. So you decide what "most ___" means, then compute
it.

Here is the menu worked for *horror*; every pattern transfers to any genre flag, and the last
three transfer to adjectives with no flag:

- *Purest label*: flagged Horror, and flagged with the fewest other genres (ties broken by
  number of ratings).
- *Biggest horror crowd*: flagged Horror, with the most ratings.
- *Horror fans' favorite*: flagged Horror, with the highest shrunk mean among users at least
  25% of whose ratings are horror films.
- *Horror by company*: the movie, flagged Horror or not, whose raters overlap most with the
  raters of the Horror-flagged catalog (for each movie, the share of its raters who also rated
  at least three Horror films). As written this ties almost everything at 100%, so it needs a
  minimum number of ratings and a stricter cutoff before it ranks anything; once it does, it
  can crown a film nobody labeled horror. That is the point. (For "most cult": the film whose
  raters rate few other films but rate this one 5.)
- *Most divisive fright*: flagged Horror, with the highest standard deviation of ratings,
  among movies with at least 20 ratings. (For "most divisive" on its own, drop the flag.)
- *Horror by name*: a title containing a word from a list you write (Halloween, Nightmare,
  Dead, Scream, ...). Crude, and worth trying once to see what it misses. (For "most 90s":
  release year is in `u.item`, but "most 90s" is not "released in the 90s"; say what it is.)

If a term in that menu is new to you (a shrunk mean, a standard deviation, co-raters), ask
Claude to explain it in plain words before you choose; a definition you cannot read is not
yours. Write your adjective on the `**My adjective:**` line (the same word you will type after
`most`) and your definition, in one sentence precise enough that a classmate could code it, on
the `**My definition:**` line; commit. Show
the top 5 under your definition and the top 5 under one other definition for the same
adjective, and say whether they agree. Then, in at most 150 words: what your definition
captures and what it misses. On its own line, say where you think "___-ness" actually lives in
this dataset: in the labels (`u.item`), in the crowd's behavior (`u.data`), or in the text of
the titles, and why. That question comes back in Collective Traces (similarity from co-rating), in Retrieval (text), and
in Alignment (whose labels count).

**Ask Claude cold, for both.** `uv run python cold_session.py best`, then `uv run python
cold_session.py most <your adjective>`. Each starts a fresh Claude outside this repo with the
file description and nothing else, and asks the question exactly as quoted above. For
each, record in a short paragraph which rule or definition Claude used, whether it told you it
had made a choice, and whether its answer came from code you can run or from memory (find the
code that prints the film; if there is none, it was recalled). If Claude's "most ___" film is
not in either of your top 5s, that is a third definition; name it. If Claude gave code and no
film, run the code in `part3.py` and report what it crowns.

### Part 4. Your own question (about 45 minutes; Claude allowed for everything except the interpretation)

Ask one descriptive question about this collective of raters and write it on the
`**Question:**` line. A menu, or bring your own: does a movie's mean rating change with how
many people rated it; do people who rate a lot rate differently from people who rate a little;
how did average ratings drift over the seven months; do genres differ in how much people
disagree. `part4.py` produces one plot (not a table), saved to `figures/part4.png`, with
labeled axes and a title, and at most 150 words of interpretation in your own words with at
least one explicit limitation (sample size, who is in this crowd, no causal claim) and one
sentence on what evidence would change your mind. `part4.py`
also has a `check()` that recomputes one number shown in the plot by a different route (a
hand-filtered slice, a different pandas path, a manual count on a small subset) and prints
MATCH or MISMATCH with both values; say in `WRITEUP.md` which it was. If you use the age,
gender, or occupation columns, be careful: 943 people who used one website in 1997 are not a
sample of anyone, and I grade the honesty of the limitation, not the finding.

### Part 5. Collaboration record (about 30 minutes, written by you)

Fill in every field of `RECORD.md`. Claude does not write here; `CLAUDE.md` keeps it out. Then:

1. In your working folder: if the transcript hook was ever declined, run
   `uv run python dump_transcript.py`. Run `uv run python sync_upstream.py` so you have the
   latest template fixes, then `uv run python run_all.py`, and fix anything it fails. Commit
   and push.
2. In a different folder, clone your repo fresh (`git clone <your repo url> hw0-check`), then
   inside it run `uv sync`, `uv run python load_data.py`, and `uv run python run_all.py`. It
   has to pass there; if it does not, fix it in your working folder, push again, and repeat.
3. Submit the repo URL (below).

One last question to carry into HW1, which asks the same kinds of questions of ten million
ratings: what in your scripts breaks when the table is a hundred times bigger?

## Required files and commit order

| File | What it holds | Written by |
|---|---|---|
| `WRITEUP.md` | the header, Part 1 answers and stuck-notes, the reconciliation table, 3a, 3b, the cold paragraphs, Part 4 | you (Claude may paste computed tables and the figure link) |
| `part1.py` | your solo code | you, before the marker |
| `cold/part2.md`, `cold/part2.jsonl`, `part2_claude.py` | the second analyst's Part 2 session (readable and raw) and its script, unchanged except for `# Fix:` lines | `cold_session.py` |
| `part2_checks.py` | one function per reconciliation row that computes the deciding evidence | you specify, Claude may code |
| `part3.py` | the two top-10s and the two top-5s | you and Claude |
| `cold/best.md`, `cold/most-<adjective>.md` (and their `.jsonl`) | Claude's cold answers to the Part 3 questions | `cold_session.py` |
| `part4.py`, `figures/part4.png` | your question's plot and its `check()` | you and Claude |
| `RECORD.md` | the eight-field collaboration record | you |
| `TRANSCRIPT.md` | every Claude Code session in this folder | the Stop hook |

Commit order, which `run_all.py` checks: `Part 0 done`, then `Part 1 finished`, then the
Part 2 capture, then everything else.

## Claude rules

**Required**

- Part 2 and Part 3's cold answers come only from `cold_session.py`; the captures in `cold/`
  are committed unedited, and `part2_claude.py` is run as given with any fix marked `# Fix:`.
- Every number in your prose comes from a script in this repo, named
  (`part2_checks.py::function`, `part3.py`, `part4.py`), or from a capture you cite.
- Complete every field of the record, including one thing you could not verify (or a justified
  "none") and any fix you made to Claude's code.
- Say what Claude wrote: `TRANSCRIPT.md` is the record of every in-repo session, and a
  `# Claude:` comment above any function Claude wrote (or one line at the top of the file if all
  of it is Claude's) is the label a grader can see without reading the transcript.

**Allowed**

- After the `Part 1 finished` commit: explanations of pandas concepts, error messages, the
  MovieLens file formats, and of your own `part1.py`.
- Part 4: writing or debugging code, suggesting questions from the menu, critiquing your plot,
  proposing limitations. You write the interpretation.
- Coding a rule or a definition you have already written on its line in `WRITEUP.md`.
- Letting Claude read the three ML-100K files (public, anonymized), your own code, and your own
  prose.
- Asking Claude to check the form of a paragraph you already wrote (the word cap, whether every
  number has a source, whether the limitation is there), if you say so in the record. Feedback
  on the reasoning is not allowed; see below.
- Asking Claude in the repo to run `cold_session.py` for you.

**Prohibited**

- Part 1: any AI, for any purpose, before the marker commit. That includes "just check my
  code."
- Claude drafting, editing, or giving feedback on the reconciliation verdicts and mechanisms,
  the best-movie defense, the "most ___" adjective, definition, and reflection, the Part 4
  interpretation, or the record. (Claude may help you *code* a definition you have already
  written down; it may not choose it.) Those are the graded reasoning, and they are yours.
- Reporting a number Claude recalled instead of one a script computed.
- Editing `part2_claude.py` beyond import or path fixes, or anything in `cold/`.
- Any prediction or held-out evaluation (train/test splits, error metrics, recommender code).
  That is HW1; doing it here is out of scope and ungraded.
- Pasting a classmate's code, captures, or transcript into Claude, or sharing yours with them.
  HW0 is individual. Talking through approaches on Slack is fine; name anyone who helped.
- A public repo. The data license and your classmates' work both say private.

## Claude collaboration record

The eight fields are in `RECORD.md`: tool and access; what I asked Claude to do; what I
checked, and how; what I accepted, rejected, or changed, and why; consequential decisions I
made myself; one thing I could not verify; what I learned, with hours; people who helped. They
are the syllabus's account of AI contributions, and later assignments ask for the same kind of
record.

## Deliverables and how to submit

- One private repo created from this template, with the files above, `run_all.py` passing on
  a fresh clone, and `TRANSCRIPT.md` and `cold/` committed.
- Submit the repo URL via HW0 on Moodle **[DECIDE: Moodle assignment URL; GitHub Classroom or
  instructor as collaborator]** by **Thu Sep 17, 8:00am Central**.
- Background Survey completed and `#comp440-f26` joined (checked under the record line of the
  rubric, not graded separately).
- The late-homework pass works as usual: once in the semester, up to three days, tell me before
  the original deadline.

## Rubric

| Criterion | Weight | Full credit looks like |
|---|---|---|
| **Part 1: You first** (the refresher) | 20 | All four questions attempted with your own code that runs; (a)–(c) correct; (d) correct or off only by a defensible reading of the spec; any unfinished question has a specific stuck-note (what you tried, where it broke); `part1.py` as of the `Part 1 finished` commit is non-empty and unchanged afterwards, and the record attests no AI before it. |
| **Part 2: Claude second and reconciliation** | 25 | `cold/part2.md` present and `part2_claude.py` differs from it only by `# Fix:` lines; row 0 matches the README and says so; a row per question with a verdict; every row names an evidence function that computes the deciding number rather than asserting it; every FAILS has a mechanism; the same-method line names a real difference between the two scripts or what was compared to find none; stuck-note questions are explained in your own words and checked; one "could not verify" claim with a reason (or a justified "none"). A wrong verdict with a sound evidence function earns most of the row; an all-HOLDS table with evidence behind every row earns the line. |
| **Part 3: Two questions with no right answer** | 25 | (a) A rule stated precisely; a defense of at most 150 words naming one gain and one loss; top-10 shown under it and under one alternative; two or three sentences on which films moved and why. (b) An adjective and a one-sentence definition of "most ___" a classmate could code; top 5 under it and under a rival definition, with whether they agree; a reflection of at most 150 words that names what the definition captures and misses and says where "___-ness" lives in the data. Claude's cold answers to both, each with its rule, whether it disclosed the choice, and computed vs recalled. Full credit does not depend on which adjective or definition you chose. |
| **Part 4: Your own question** | 15 | A one-sentence question about the collective of raters; a plot (not a table) with labeled axes and a title that answers it; at most 150 words of interpretation in your own words with at least one explicit limitation and a sentence on what evidence would change your mind; a `check()` that recomputes one plotted number by a different route and matches (or explains the mismatch). |
| **Part 5: Record, setup, and repo hygiene** | 15 | All eight record fields filled specifically (function names for checks, real decisions, real hours); the "learned" paragraph is in your own voice; `TRANSCRIPT.md` and the `cold/` captures committed and unedited; `run_all.py` passes on a fresh clone; the commit history shows `Part 0 done`, then `Part 1 finished`, then everything else; survey done and Slack joined. |
| | **100** | |

A record that says "checked, fine" with no method earns partial credit at most on the lines it
touches.

## If you would rather not use Claude (opt-out)

You may opt out of Claude for this assignment with no reason given and no grade effect. Talk
with me by Fri Sep 11 (after class, office hours, email, or a Slack DM), as the syllabus says. You
do the same repo with a second analyst that is not an AI you operate: my Reference Analyst
pack, which is Claude's cold answers to the Part 2 and Part 3 questions, captured once by me
with the same tool, unchanged, errors and all. I send it to you privately on request;
`uv run python cold_session.py --import reference-analyst.zip` installs it into `cold/` and
`part2_claude.py`. **[DECIDE: the pack's "most ___" capture is for horror; either that is the
adjective opt-out students report on, or I run one capture per opt-out adjective on request.]**
You run Claude's script as given, build the same reconciliation table, adjudicate divergences with
the same evidence functions, and complete the same record (field 2 becomes "what the Reference
Analyst claimed"; field 6 becomes a claim in that capture you could not verify). For Part 4 you
use documentation, the pandas reference, Slack, and office hours; the `check()` is still
required. The rubric is unchanged. What you practice is identical except for one thing: you
will not get the experience of directing a model, which the Sep 17 debrief partly gives back,
since I release the Reference Analyst pack to the whole class that day.

## If Claude (or something else) is down

Per the syllabus, a reported access problem never costs you points.

- You declined the transcript hook: run `uv run python dump_transcript.py` before committing.
- `claude` is missing, or print mode is refused on your account: `uv run python
  cold_session.py --show-prompt best` prints the exact prompt, and `--interactive best` opens
  a cold session for you to paste it into; copy the reply into `cold/best.md` by hand and say
  "manual capture" in the record.
- Claude is down, or your course account is not working: post in `#comp440-f26` or email me,
  install the Reference Analyst pack with `--import` for Parts 2 and 3 exactly as in the
  opt-out path, do Part 4 without AI, and note in the record which parts used the fallback and
  when. If an outage lasts more than about half a day during Sep 10–17, I extend the deadline
  for everyone by 48 hours **[DECIDE: 24 or 48]**, without spending your late-homework pass; a
  student-specific access failure reported before the deadline gets the same extension.
- `git push` or `git clone` asks for a password: GitHub no longer accepts account passwords;
  log in with `gh auth login` (or the method on the install page) and try again.
- GitHub is down at the deadline: email me a zip of the repo without `data/`.
- On Windows and something behaves differently from this brief (paths that start with `C:` or
  `/c/`, `uv` not found, the hooks never firing): you are not in WSL2. Open the Ubuntu terminal,
  keep the repo under your Ubuntu home, and start again from `git clone`.
- Your laptop cannot run WSL2 (virtualization disabled and locked, or an old Windows) or cannot
  run `uv` or Python 3.13: tell me by Fri Sep 11 **[DECIDE: lab machine, Codespace, or
  loaner]**.

## FAQ

**Why won't Claude look at my Part 1 before I commit?** Working as intended. Part 1 is yours
alone; the commit is how you say you are done.

**`cold_session.py` refuses to run. Why?** It tells you: Part 1 is not committed; your
`**My rule:**` (or `**My adjective:**` and `**My definition:**`) line is empty or not committed;
or that capture already exists (use `--again` and say in the record which one you used).

**I committed Part 1 and Claude still refuses.** Check `git log --oneline` for a message that
starts with `Part 1 finished`. If yours does not, `git commit --allow-empty -m "Part 1
finished"`.

**`load_data.py` or `run_all.py` says `origin` is the template, or is missing.** You are
working in a clone of the template itself (or in an unzipped download). Create your own
private repo from the template, clone that, and copy your files over; your work belongs in
your repo.

**Claude says the template has updates.** Say yes and it runs `uv run python
sync_upstream.py` for you, or run it yourself. Your files are never overwritten; see "How this
repo works".

**Can I use PowerShell or Git Bash on Windows instead of WSL2?** No. The assignment was tested
on Linux, and WSL2 is Linux; anything else is unsupported and I cannot help you debug it.

**`claude` keeps asking permission for `git log` and `ls`.** The repo pre-approves the
read-only commands it runs at the start of every session (`.claude/settings.json`); if you
declined the project settings on first launch, run `claude` again and accept them.

**Claude refused to pick my rule or my adjective for me.** Working as intended. Choosing is the
assignment.

**Can Claude write my code?** Yes, in Parts 2–4, if you direct it; never in Part 1, and never
as the second analyst, which is what `cold_session.py` is for.

**Claude's cold answer was right about everything.** Fine, if every row has evidence behind it.

**Claude's cold script crashed.** See Part 2: fix import or path errors only; anything else is
a finding.

**Can I ask Claude in the repo to run `cold_session.py` for me?** Yes. The call shows up in
`TRANSCRIPT.md`.
