# COMP 440, HW0: Working With Data and Claude — An AI and Human Analyst

**Fall 2026 · Individual · 6% of the course grade**
**Due Thu Sep 17, 8:00am Central**

Aim to finish Parts 1–3 by Mon Sep 14. HW1 goes out Tue  Sep 15 and builds on this, so finish HW0 first.

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
> adopts a collaboration record (its repo currently ships DECISIONS.md and REFLECTION.md and
> uses ML-10M). HW0's record is now the last section of `WRITEUP.md`; `RECORD.md` is gone.
> Windows: WSL2 (Ubuntu) is required, per your Sep 5 decision, so Windows students run the
> exact Linux path tested here; native Windows, PowerShell, and Git Bash are unsupported. The
> install page must cover the WSL2 steps (Store install, reboot, virtualization enabled in
> firmware, Ubuntu username and password, VS Code WSL extension, repo under the Ubuntu home).
> Worth one dry run on a Windows laptop before Sep 10 anyway, mainly for the Claude Code login
> inside WSL2 on the course account type. The session-start hook fetches this template from
> GitHub each time `claude` starts (silent when offline), and Claude merges fixes you
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
Afterward, you will work together to compare your findings. 


In this assignment you will analyze the [MovieLens 100K](https://grouplens.org/datasets/movielens/100k/) dataset, which contains 100,000 ratings of 1–5 stars that 943
anonymous people gave 1,682 movies in 1997–98.  
`load_data.py` unzips the checked-in `ml-100k.zip` and reads them  into plain records, with a pandas conversion for each.
This work will feed into HW1, where you analyze a much larger and more complex dataset.

## How this activity will work

1. You complete parts 1, 2 and 3 on your own (`human_part1.py`, `human_part2.py`,
   `human_part3.py`). You can ask Claude for debugging and install help, but nothing else.
2. Claude answers the same three questions on its own (in `claude_answers_1_2_3.py`), without
   seeing your code or your answers.
3. You and Claude work through the differences together.

You write your answers in `WRITEUP.md`. Claude records the transcript of your sessions to share
with Shilad.

## The task

### Part 0. Setup (in class Thu Sep 10)

1. Complete `INSTALL.md`.
2. Fork this repo and clone your fork.
3. In the clone, start `claude`, approve the hooks, and type `/setup`. Claude does the rest and
   asks your name.

Tell me on `#comp440-f26` by Fri Sep 11 if anything does not work.

### Parts 1–3. Your answers (no Claude, except for debugging)

Each script says what it must produce. Write your answers in `WRITEUP.md`.

**Part 1, `human_part1.py`** — basic statistics: how much data there is, how ratings are spread,
which movies got the most ratings, and which rate highest among movies with at least 20 ratings.

**Part 2, `human_part2.py`** — the best movie. There is no single answer: it depends on how you
combine 943 people's judgments. Choose a rule and defend it.

**Part 3, `human_part3.py`** — the most XYZ movie. Pick an adjective XYZ anything non-trivial you can define.
Nothing in the data answers this directly, so you decide what the word means, then compute it.

Ask Claude for help installing things and for help when something breaks. Not for the analysis,
the rule, the adjective, or the definition. Those are what you are being graded on.

When all three run and your Part 1–3 answers are written, ask Claude to check them over. It
will run your scripts, tell you what is missing, and help you fix what does not work. Then it
asks whether you are ready to hand Parts 1–3 in, and commits them when you say yes.

Parts 1–3 are graded as they stood at that commit, so say yes when you mean it.

### Part 4. Claude's turn

Ask Claude to answer the same three questions. It starts a separate session in an empty
directory holding only the data, the loader, and an empty `claude_answers_1_2_3.py` . 
It has no access to your code, your answers, or your conversation. It gets the questions from
`questions.md`, word for word, so that every student's Claude is asked the same thing.

Read what it wrote before you go on.

### Parts 5–6. Working through the differences

**Part 5** — the best movie. What rule did Claude choose? Did it tell you it was choosing, or
present its answer as *the* answer? Where do your two lists differ, and why? Then decide whose
rule is better, and for what. You are allowed to conclude that Claude's is.

**Part 6** — the most ___ movie. Same questions for your adjective. If Claude's film is not in
your top 5, it used a definition you had not thought of: name it.

Claude can compute anything you ask it to here. The judgments are yours.

Finally, answer the last few questions in `WRITEUP.md`. Ask Claude to check the submission
over; it will walk through what is missing. Then commit, push, and fill in the form:

https://docs.google.com/forms/d/e/1FAIpQLSfC1Dr1js4kP91O11uqCbpRh4B2ifgxeJb3TPYKbd4QLmoFzw/viewform

Tell Claude when you have. It will say **YOU ARE FINISHED!** — that is how you know you are
done. Due **Thu Sep 17, 8:00am Central**.

One question to carry into HW1: what in your scripts breaks when the data is a hundred times
bigger?

## Claude rules

**Yours alone:** the analysis in Parts 1–3, and every judgment in `WRITEUP.md` — the rule, the
adjective, the definitions, and what you conclude in Parts 5 and 6. Claude does not draft,
edit, or give feedback on any of it.

**Claude's alone:** `claude_answers_1_2_3.py` and `questions.md`. Neither is edited by anyone.

**Also:** no AI at all in the analysis for Parts 1–3, autocomplete included. Every number in
your writeup comes from a script you can name. Do not share code or answers with classmates —
talking through approaches is fine, and name anyone who helped. Keep your repo private.

## Rubric

| Part | Weight | Full credit |
|---|---|---|
| **1. Basic statistics** | 20 | Your own code, and it runs; correct answers, with anything you got stuck on written down. |
| **2. The best movie** | 20 | A rule precise enough to code, defended with what it gains and loses. |
| **3. The most ___ movie** | 20 | A definition a classmate could code, and an honest account of what it misses. |
| **4. Claude's turn** | 5 | Claude's answers committed unedited. |
| **5–6. Working through the differences** | 30 | You say what Claude chose and whether it admitted choosing; you explain where the answers diverge; you reach a judgment and defend it. |
| **Working with Claude** | 5 | Honest answers about what you asked for and what you could not verify. |
| | **100** | |

## Talk to me if...

**You notice something is odd or confusing.** This activity is our first Claude experiment!

**You would rather not use Claude.** Talk to me by Fri Sep 11; there is no grade effect.

**Claude, or something else, is down.** A reported problem never costs you points — post in
`#comp440-f26` or email me. An outage of more than about half a day extends the deadline by 48
hours.

**Claude refuses to pick your rule or adjective, or to help with the analysis.** Working as
intended; choosing is the assignment.
