"""
Part 1: basic rating statistics.

    uv run python human_part1.py

Answer the four questions below with your own code, print each answer under its label, and
explain each in one sentence in WRITEUP.md.
"""

from load_data import load_all


def human_part1(ratings, ratings_df, movies, movies_df, users, users_df):
    print("part 1 unimplemented")  # delete this line when you start

    print("== (a) ==")
    # (a) How many ratings, users, and movies are there, and how are ratings distributed across 1-5 stars?

    print("== (b) ==")
    # (b) What is the median number of ratings per user, and how many users have 100 or more ratings?

    print("== (c) ==")
    # (c) Join ratings to titles. Which 10 movies have the most ratings?

    print("== (d) ==")
    # (d) Among movies with at least 20 ratings, which 10 have the highest mean rating?
    #     Show title, mean, and count.


if __name__ == "__main__":
    ratings, ratings_df, movies, movies_df, users, users_df = load_all()
    human_part1(ratings, ratings_df, movies, movies_df, users, users_df)
