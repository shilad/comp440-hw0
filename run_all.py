"""
Run the whole assignment, start to finish.

    uv run python run_all.py

Unzips the data if needed, reads it, says how much there is, then runs parts 1 to 4. Each
part is a function in its own file and also runs alone: uv run python part3.py.
"""

import traceback

from load_data import read_movies, read_ratings, read_users, unzip_if_needed
from part1 import part1
from part2_checks import part2
from part3 import part3
from part4 import part4

unzip_if_needed()
movies = read_movies()
ratings = read_ratings()
users = read_users()
print(f"{len(ratings):,} ratings, {len(movies):,} movies, {len(users):,} users")

for part in (part1, part2, part3, part4):
    print(f"\n== {part.__name__} ==")
    try:
        part()
    except Exception:
        # A crash in one part must not hide the others; part 1 stays as committed even if it crashes.
        traceback.print_exc()
        print(f"{part.__name__} crashed; see the traceback above")
