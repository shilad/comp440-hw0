"""
Run your half of the assignment, start to finish.

    uv run python run_all.py

Reads the data once, says how much there is, then runs parts 1, 2, and 3. Each part is a
function in its own file and also runs alone: uv run python human_part2.py.
"""

from human_part1 import human_part1
from human_part2 import human_part2
from human_part3 import human_part3
from load_data import load_all

ratings, ratings_df, movies, movies_df, users, users_df = load_all()
print(f"{len(ratings):,} ratings, {len(movies):,} movies, {len(users):,} users")

human_part1(ratings, ratings_df, movies, movies_df, users, users_df)
human_part2(ratings, ratings_df, movies, movies_df)
human_part3(ratings, ratings_df, movies, movies_df)
