"""
Part 3: two questions with no right answer. Prints the two top-10s (3a) and the two top-5s (3b)
that the tables in WRITEUP.md hold.

    uv run python part3.py

Claude codes this only after your rule (3a) and your adjective and definition (3b) are written
on their lines in WRITEUP.md and committed. The four functions below are named for the four
WRITEUP.md labels; WRITEUP.md names the function that printed any number you quote. Put a
`# Claude:` comment above any function Claude wrote.

3a. The best movie. "What is the best movie in this dataset?" depends on how you combine 943
people's judgments. Choose a rule and state it precisely:
  - the plain mean;
  - the mean among movies with at least N ratings, an N you choose;
  - the number of ratings;
  - a shrunk mean, score = (n * mean + k * global_mean) / (n + k), with a k you choose and
    defend. None is recommended; your defense says what a larger or smaller k would do.
Print the top 10 under your rule and under the alternative rule: title, score, and count.

3b. The most ___ movie. Nothing in the files answers "Which movie is the most ___?" directly:
a flag of 1 or 0 is not "more" or "less," Horror|Comedy|Romance is arguably less horror than
Horror alone, and "cult" or "90s" has no flag at all. You decide what "most ___" means, then
compute it. The menu, worked for horror; the last three need no flag:
  - Purest label: flagged Horror with the fewest other genres, ties broken by rating count.
  - Biggest crowd: flagged Horror with the most ratings.
  - Fans' favorite: flagged Horror with the highest shrunk mean among users at least 25% of
    whose ratings are horror.
  - By company: any movie, flagged or not, whose raters overlap most with Horror's raters (the
    share who also rated at least three Horror films). As written this ties almost everything
    at 100%; with a minimum count and a stricter cutoff it ranks, and can crown a film nobody
    labeled horror. That is the point.
  - Most divisive: flagged Horror with the highest standard deviation of ratings, at least 20
    ratings. Drop the flag for "most divisive" alone.
  - By name: a title containing a word from a list you write (Halloween, Nightmare, Dead,
    Scream). Crude, and worth one try to see what it misses.
"Most cult" might be the film whose raters rate few other films but rate this one 5; "most
90s" is not "released in the 90s," so say what it is. The rival definition is for the same
adjective. Print the top 5 under each: title, the score the definition uses, and count.
"""

from load_data import (movies_to_pandas, ratings_to_pandas, read_movies, read_ratings,
                       read_users, users_to_pandas)


def top10_my_rule(ratings, movies):
    """3a, the `**My rule:**` line: title, score, and count."""
    print("== 3a: top 10 under my rule ==")


def top10_alternative_rule(ratings, movies):
    """3a, the `**Alternative rule:**` line."""
    print("== 3a: top 10 under the alternative rule ==")


def top5_my_definition(ratings, movies):
    """3b, the `**My definition:**` line: title, the score the definition uses, and count."""
    print("== 3b: top 5 under my definition ==")


def top5_rival_definition(ratings, movies):
    """3b, the `**Rival definition:**` line."""
    print("== 3b: top 5 under the rival definition ==")


def part3():
    print("part 3 unimplemented")  # delete this line when you start
    ratings = ratings_to_pandas(read_ratings())   # user_id, movie_id, rating, timestamp
    movies = movies_to_pandas(read_movies())      # movie_id, title, release_date, imdb_url, a True/False column per genre
    users = users_to_pandas(read_users())         # user_id, age, gender, occupation, zip_code

    top10_my_rule(ratings, movies)
    top10_alternative_rule(ratings, movies)
    top5_my_definition(ratings, movies)
    top5_rival_definition(ratings, movies)


if __name__ == "__main__":
    part3()
