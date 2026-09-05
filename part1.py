"""
Part 1: you first. Solo, 45 minutes, no AI of any kind (that includes "just check my code").

    uv run python part1.py

Answer the four questions below with your own pandas code and print the answers under the
labels. Put one sentence of explanation per answer in WRITEUP.md, Part 1. If a question is
unfinished when the timer runs out, leave what you have in a comment block, write
`# STUCK (d): what I tried / where it broke` above it, and put the same stuck-note in
WRITEUP.md. A stuck-note earns credit; a blank does not. The file must still run.

When you stop, write the finish time on the `**Part 1 finished:**` line of WRITEUP.md and
commit, yourself, with a message that starts with the words "Part 1 finished":

    git add part1.py WRITEUP.md
    git commit -m "Part 1 finished"

That commit is the marker. Until it exists, Claude in this repo will not touch analysis
code or this file (see CLAUDE.md and .claude/hooks/guard.py); after it, Claude may read this
file and explain it, but never edits it. Part 1 is graded as it was at that commit.
"""

from load_data import load_movies, load_ratings, load_users

ratings = load_ratings()   # user_id, movie_id, rating, timestamp
movies = load_movies()     # movie_id, title, release_date, video_release_date, imdb_url, 19 genre flags
users = load_users()       # user_id, age, gender, occupation, zip_code

print("== (a) ==")
# (a) How many ratings, users, and movies are there, and how are ratings distributed across 1-5 stars?


print("== (b) ==")
# (b) What is the median number of ratings per user, and how many users have 100 or more ratings?


print("== (c) ==")
# (c) Join ratings to titles. Which 10 movies have the most ratings?


print("== (d) ==")
# (d) Among movies with at least 20 ratings, which 10 have the highest mean rating?
#     Show title, mean, and count.

