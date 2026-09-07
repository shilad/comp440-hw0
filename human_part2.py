"""
Part 2: the best movie.

    uv run python human_part2.py

Write your rule on the `**My rule:**` line of WRITEUP.md and a second, different rule on the
`**Alternative rule:**` line. Print the top 10 movies (id, title, ratings count, mean rating)
under each.
"""

from load_data import load_all


def top10_my_rule(ratings, ratings_df, movies, movies_df):
    print("== My rule ==")


def top10_alternative_rule(ratings, ratings_df, movies, movies_df):
    print("== Alternative rule ==")


def human_part2(ratings, ratings_df, movies, movies_df):
    print("part 2 unimplemented")  # delete this line when you start
    top10_my_rule(ratings, ratings_df, movies, movies_df)
    top10_alternative_rule(ratings, ratings_df, movies, movies_df)


if __name__ == "__main__":
    ratings, ratings_df, movies, movies_df, users, users_df = load_all()
    human_part2(ratings, ratings_df, movies, movies_df)
