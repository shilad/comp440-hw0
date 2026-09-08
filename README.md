# COMP 440, HW0: Working With Data and Claude — An AI and Human Analyst

**Fall 2026 · Individual · 6% of the course grade**
**Due Thu Sep 17, 8:00am Central**

Aim to finish Parts 1–3 by Mon Sep 14. HW1 goes out Tue Sep 15 and builds on this, so finish HW0 first.

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
combine 943 people's judgments. Choose a rule, defend it, and say what you rejected on the
way.

**Part 3, `human_part3.py`** — the most XYZ movie. Pick an adjective XYZ anything non-trivial you can define.
Nothing in the data answers this directly, so you decide what the word means, then compute it,
and say what you rejected on the way.

Ask Claude for help installing things and for help when something breaks. Not for the analysis,
the rule, the adjective, or the definition. Those are what you are being graded on.

When all three run and your Part 1–3 answers are written, ask Claude to check them over. It
will run your scripts, tell you what is missing, and help you fix what does not work. Then it
asks whether you are ready to hand Parts 1–3 in, and commits them when you say yes.

### Part 4. Claude's turn

Ask Claude to answer the same three questions. It starts a separate session in an empty
directory holding only the data, the loader, and an empty `claude_answers_1_2_3.py` . 
It has no access to your code, your answers, or your conversation. It gets the questions from
`questions.md`, word for word, so that every student's Claude is asked the same thing.

Read what it wrote before you go on.

### Parts 5–6. Working through the differences

**Part 5** — the best movie. What rule did Claude choose? Read its code: does it anywhere admit
a different rule was possible, or does it give its answer as simply the answer? Where do your
two best-movie lists differ, and why? Then decide whose
rule is better, and for what. You are allowed to conclude that Claude's is.

**Part 6** — the most ___ movie. Same questions for your adjective. If Claude's film is not in
your top 5, it used a definition you had not thought of: name it.

Claude can analyze, explain, and compute anything you ask it to here. The judgments are yours.

Finally, answer the last few questions in `WRITEUP.md`. Ask Claude to check the submission
over; it will walk through what is missing. Then commit, push, and fill in the form:

https://forms.gle/DMHxZsafEr92fTfK6

Tell Claude when you have. It will say **YOU ARE FINISHED!** — that is how you know you are
done. Due **Thu Sep 17, 8:00am Central**.

One question to carry into HW1: what in your scripts breaks when the data is a hundred times
bigger?

## AI guidelines

**No AI**: the analysis for Parts 1–3, though you can ask Claude for debugging help. The
words in `WRITEUP.md` are yours throughout — Claude never drafts, edits, or rewords them.
Every number in it comes from a script you can name.

**Never edited by anyone**: `claude_answers_1_2_3.py` and `questions.md`.

**AI encouraged**: For installation (part 0), part 5, and part 6, including any comparative analyses.

## Rubric

For this assignment I'll grade your process (via your transcript with Claude), your code,
and your answers.

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
