"""
Part 2: the evidence behind the reconciliation table. One check function per row.

    uv run python part2_checks.py

A check function recomputes the number a row turns on, from the data, by a route you can
read, and prints it next to what each analyst's script printed. It does not decide anything:
the Verdict cell is yours, and the function's job is to put the deciding number in front of
you. So a check computes; it never asserts. `assert n == 100000` or `print("HOLDS")` proves
only that you typed the number you expected, and rerunning either script's code is not
evidence either: the same code prints the same wrong number twice. A route worth taking
differs from both scripts: the records instead of the DataFrame, the raw file instead of
`load_data.py`, the other join key, or a statistic recomputed from its definition. When a row
is about a reading of the spec (what "at least 20" means, how ties break, title or id), the
check computes the answer under each reading and prints both, so you can see which one the
data supports.

Name each function for its row (check_row0, check_a, check_d_ties); the table's Evidence cell
cites `part2_checks.py::check_a`. Put a `# Claude:` comment above any function Claude wrote.
part2() calls every check, so one run prints all the evidence at once. The worked example is
the warm-up question from class.
"""

from load_data import (movies_to_pandas, ratings_to_pandas, read_movies, read_ratings,
                       read_users, users_to_pandas)


def check_warmup():
    """Warm-up from class: how many ratings are exactly 5 stars? The cold Claude answered from
    memory. This counts over the Rating records rather than the DataFrame the scripts use:
    a different route, which is what makes it evidence. You compare the two numbers."""
    n = 0
    for r in read_ratings():
        if r.rating == 5:
            n += 1
    print(f"check_warmup: ratings that are exactly 5 stars = {n:,}")
    return n


# check_row0(ratings, movies): the README's counts (100,000 / 943 / 1,682 / every user at
# least 20 ratings), recomputed here, printed next to what part2_claude.py printed for (a).


# check_a, check_b, check_c, check_d: one per question, plus a second function for any row
# that needs one (check_d_threshold, check_d_ties).


def part2():
    print("part 2 unimplemented")  # delete this line when you start
    ratings = ratings_to_pandas(read_ratings())   # user_id, movie_id, rating, timestamp
    movies = movies_to_pandas(read_movies())      # movie_id, title, release_date, imdb_url, a True/False column per genre
    users = users_to_pandas(read_users())         # user_id, age, gender, occupation, zip_code

    check_warmup()


if __name__ == "__main__":
    part2()
