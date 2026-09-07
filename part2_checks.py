"""
Part 2: the evidence behind the reconciliation table. One check function per row.

    uv run python part2_checks.py

A check function recomputes the number a row turns on, from the raw data, by a route you can
read, and prints it next to what each analyst's script printed. It does not decide anything:
the Verdict cell is yours, and the function's job is to put the deciding number in front of
you. So a check computes; it never asserts. `assert n == 100000` or `print("HOLDS")` proves
only that you typed the number you expected. When two scripts disagree, the check settles it
by computing the value and showing it; when a row is about a reading of the spec (what "at
least 20" means, how ties break, title or id), it computes the answer under each reading and
prints both, so you can see which one the data supports.

Name each function for its row (check_row0, check_a, check_d_ties); the table's Evidence cell
cites `part2_checks.py::check_a`. Put a `# Claude:` comment above any function Claude wrote.
Every function is called from the main block, so this file prints all the evidence at once.
The worked example is the warm-up question from class.
"""

from load_data import load_movies, load_ratings, load_users

ratings = load_ratings()   # user_id, movie_id, rating, timestamp
movies = load_movies()     # movie_id, title, release_date, video_release_date, imdb_url, 19 genre flags
users = load_users()       # user_id, age, gender, occupation, zip_code


def check_warmup():
    """Warm-up from class: how many ratings are exactly 5 stars? The cold Claude answered from
    memory; this computes it. You compare the two."""
    n = int((ratings["rating"] == 5).sum())
    print(f"check_warmup: ratings that are exactly 5 stars = {n:,}")
    return n


# check_row0: the README's counts (100,000 / 943 / 1,682 / every user at least 20 ratings),
# recomputed here, printed next to what part2_claude.py printed for (a).


# check_a, check_b, check_c, check_d: one per question, plus a second function for any row
# that needs one (check_d_threshold, check_d_ties).


if __name__ == "__main__":
    check_warmup()
