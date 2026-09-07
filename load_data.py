"""
The MovieLens 100K data, read into plain Python records.

    uv run python load_data.py      # unzips ml-100k.zip on first use and prints the counts

Three readers, one per file, each returning a list of records:

    ratings = read_ratings()    # list[Rating]  from u.data
    movies = read_movies()      # list[Movie]   from u.item
    users = read_users()        # list[User]    from u.user

and three conversions for when you want pandas:

    ratings_df = ratings_to_pandas(ratings)    # one row per Rating
    movies_df = movies_to_pandas(movies)       # one True/False column per genre
    users_df = users_to_pandas(users)

A DataFrame is one way of holding the same data, not the data itself: groupby, merge, and
sort live there, and the records are what it is built from.
"""

from __future__ import annotations

import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent
ZIP = REPO / "ml-100k.zip"            # checked into the repo
ML_DIR = REPO / "data" / "ml-100k"    # where the zip unpacks to

# The 19 genres, in the order u.item lists its flags.
GENRES = ["unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
          "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery",
          "Romance", "Sci-Fi", "Thriller", "War", "Western"]


@dataclass
class Movie:
    movie_id: int
    title: str            # with the year, e.g. "Toy Story (1995)"
    release_date: str     # e.g. "01-Jan-1995"; empty for one movie
    imdb_url: str
    genres: list[str]     # the genres flagged 1 in u.item; a movie can have several


@dataclass
class Rating:
    user_id: int
    movie_id: int
    rating: int           # 1 to 5 stars
    timestamp: int        # unix seconds


@dataclass
class User:
    user_id: int
    age: int
    gender: str           # "M" or "F"
    occupation: str
    zip_code: str         # a string: zip codes have leading zeros, and some are not numbers


def unzip_if_needed() -> None:
    """Unpack ml-100k.zip into data/ the first time anything asks for the data."""
    if (ML_DIR / "u.data").exists():
        return
    if not ZIP.exists():
        sys.exit(f"{ZIP.name} is missing; it ships with the template repo.")
    print(f"Unzipping {ZIP.name} into {ML_DIR.parent.name}/ ...")
    with zipfile.ZipFile(ZIP) as z:
        z.extractall(ML_DIR.parent)


def read_ratings() -> list[Rating]:
    """u.data: one rating per line, tab-separated: user id, movie id, rating, timestamp."""
    unzip_if_needed()
    ratings = []
    with open(ML_DIR / "u.data") as f:
        for line in f:
            user_id, movie_id, rating, timestamp = line.rstrip("\n").split("\t")
            ratings.append(Rating(int(user_id), int(movie_id), int(rating), int(timestamp)))
    return ratings


def read_movies() -> list[Movie]:
    """u.item: one movie per line, separated by |, latin-1 encoded (nine titles have accents):
    movie id, title, release date, video release date (always empty), IMDb URL, then the 19
    genre flags, 1 or 0, in the order of GENRES."""
    unzip_if_needed()
    movies = []
    with open(ML_DIR / "u.item", encoding="latin-1") as f:
        for line in f:
            fields = line.rstrip("\n").split("|")
            genres = []
            for name, flag in zip(GENRES, fields[5:]):
                if flag == "1":
                    genres.append(name)
            movies.append(Movie(int(fields[0]), fields[1], fields[2], fields[4], genres))
    return movies


def read_users() -> list[User]:
    """u.user: one user per line, separated by |: user id, age, gender, occupation, zip code."""
    unzip_if_needed()
    users = []
    with open(ML_DIR / "u.user") as f:
        for line in f:
            user_id, age, gender, occupation, zip_code = line.rstrip("\n").split("|")
            users.append(User(int(user_id), int(age), gender, occupation, zip_code))
    return users


def ratings_to_pandas(ratings: list[Rating]) -> pd.DataFrame:
    """The same ratings as a DataFrame: columns user_id, movie_id, rating, timestamp."""
    return pd.DataFrame(ratings)


def movies_to_pandas(movies: list[Movie]) -> pd.DataFrame:
    """The same movies as a DataFrame: movie_id, title, release_date, imdb_url, then one
    True/False column per genre, so df[df["Horror"]] is the horror movies."""
    rows = []
    for m in movies:
        row = {"movie_id": m.movie_id, "title": m.title, "release_date": m.release_date,
               "imdb_url": m.imdb_url}
        for genre in GENRES:
            row[genre] = genre in m.genres
        rows.append(row)
    return pd.DataFrame(rows)


def users_to_pandas(users: list[User]) -> pd.DataFrame:
    """The same users as a DataFrame: user_id, age, gender, occupation, zip_code."""
    return pd.DataFrame(users)


if __name__ == "__main__":
    unzip_if_needed()
    print(f"{len(read_ratings()):,} ratings, {len(read_movies()):,} movies, {len(read_users()):,} users")
