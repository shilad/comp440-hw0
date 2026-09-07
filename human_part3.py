"""
Part 3: the most ___ movie.

    uv run python human_part3.py

Pick an adjective. Write it on the `**My adjective:**` line of WRITEUP.md, a one-sentence
definition a classmate could code on the `**My definition:**` line, and a second, different
definition on the `**Rival definition:**` line. Print the top 5 movies under each.
"""

from load_data import load_all


def top5_my_definition(ratings, ratings_df, movies, movies_df):
    print("== My definition ==")


def top5_rival_definition(ratings, ratings_df, movies, movies_df):
    print("== Rival definition ==")


def human_part3(ratings, ratings_df, movies, movies_df):
    print("part 3 unimplemented")  # delete this line when you start
    top5_my_definition(ratings, ratings_df, movies, movies_df)
    top5_rival_definition(ratings, ratings_df, movies, movies_df)


if __name__ == "__main__":
    ratings, ratings_df, movies, movies_df, users, users_df = load_all()
    human_part3(ratings, ratings_df, movies, movies_df)
