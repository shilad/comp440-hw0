# HW0 writeup

**Title:**
**Name:**
**Assignment:** COMP 440 HW0, Fall 2026
**Date:**
**Claude:** Using Claude / Opt-out path (delete one)

Every number below comes from a file in this repo; say which file and function produced it.
Prose limits are limits: graders stop reading at the cap. Keep the bold labels exactly as they
are, on their own lines; `cold_session.py` and `run_all.py` look for them.

## Part 1: You first (solo, no AI)

Code: `part1.py`. One sentence of explanation per answer, with the numbers.

**Timer started:**

**(a) How many ratings, users, and movies are there, and how are ratings distributed across 1–5 stars?**

>

**(b) What is the median number of ratings per user, and how many users have 100 or more ratings?**

>

**(c) Join ratings to titles. Which 10 movies have the most ratings?**

>

**(d) Among movies with at least 20 ratings, which 10 have the highest mean rating? Show title, mean, and count.**

>

**Stuck-notes (what I tried, where it broke), or "none":**

>

**Part 1 finished:**

## Part 2: Claude second, then reconcile

Claude's code, run as given: `part2_claude.py` (captured in `cold/part2.md`).

**Fixes to Claude's code (import or path errors only), or "none":**

>

**Reconciliation table.** Verdicts are on Claude's answer: HOLDS, FAILS, or CANNOT DETERMINE.
Every row, HOLDS included, names the function in `part2_checks.py` that computes its deciding
evidence. Every FAILS also names a mechanism (code bug / data trap / different reading of the
spec / statistical misreading / recalled rather than computed).

| Question | Mine | Claude's | Match? | Verdict | Mechanism if FAILS | Evidence (part2_checks.py::function) |
|---|---|---|---|---|---|---|
| 0. README counts: 100,000 / 943 / 1,682 / every user at least 20 ratings (write "not printed" in Claude's column for a number its script never printed; the verdict on that is yours) | | | | | | |
| (a) | | | | | | |
| (b) | | | | | | |
| (c) | | | | | | |
| (d) | | | | | | |

**Same method? Did the two scripts compute the answers the same way (join key, filter, tie-break, title vs id)? Name one difference, or what you compared to conclude there is none:**

>

**Part 1 stuck questions, explained in my own words and checked (or "none"):**

>

**One thing Claude said that I could not verify, and why:**

>

## Part 3: Two questions with no right answer

### 3a. The best movie

**My rule:**

**Alternative rule:**

**Defense (at most 150 words: one thing my rule gains, one thing it loses):**

>

Top 10 under each rule (code: `part3.py`):

| Rank | My rule | Alternative rule |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |
| 7 | | |
| 8 | | |
| 9 | | |
| 10 | | |

**What moved between my two top-10s, and why (two or three sentences: name at least one film that is on one list and not the other, and say what my rule rewards that the alternative does not):**

>

### 3b. The most ___ movie

**My adjective:**

**My definition:**

**Rival definition:**

Top 5 under each definition (code: `part3.py`):

| Rank | My definition | Rival definition |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

**Do they agree?**

>

**Reflection (at most 150 words): what my definition captures and what it misses:**

>

**Where "___-ness" lives in this dataset (the labels in u.item, the crowd's behavior in u.data, or the text of the titles), and why:**

>

### Claude, cold

**Best movie (cold/best.md):** which rule Claude used; whether it said it was making a choice; whether the film came from code you can run or from memory, and how you know.

>

**Most ___ movie (cold/most-<adjective>.md):** the same three things.

>

**Third definition, if any (Claude's film is in neither of my top 5s):**

>

## Part 4: Your own question

**Question:**

**Plot:** `figures/part4.png` (code: `part4.py`; labeled axes and a title)

**Interpretation (at most 150 words, my own words, at least one explicit limitation, and one sentence on what evidence would change my mind):**

>

**Independent check:** what `part4.py`'s `check()` recomputes, by what different route, and whether it printed MATCH or MISMATCH (and why, if MISMATCH).

>
