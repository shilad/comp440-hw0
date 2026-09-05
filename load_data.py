"""
Load the MovieLens 100K dataset (GroupLens Research, University of Minnesota).

The zip ships with this repo (ml-100k.zip, about 5 MB), so nothing is downloaded. Run once:

    uv run python load_data.py

That unzips it into data/ml-100k/, prints the dataset's own README, and checks the three
files against the counts the README promises.

Or import from your analysis code:

    from load_data import load_ratings, load_movies, load_users

If the zip is ever missing, the script downloads it from files.grouplens.org (or from
ML100K_URL, if you set that to a mirror).
"""

from __future__ import annotations

import os
import sys
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

# Windows consoles are not always UTF-8; never let a stray character crash a student's run.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

REPO_ROOT = Path(__file__).resolve().parent
DATA_DIR = REPO_ROOT / "data"
ML_DIR = DATA_DIR / "ml-100k"
ZIP_PATH = REPO_ROOT / "ml-100k.zip"          # checked into the repo
DOWNLOADED_ZIP = DATA_DIR / "ml-100k.zip"     # only if the checked-in zip is missing
ZIP_URL = os.environ.get("ML100K_URL", "https://files.grouplens.org/datasets/movielens/ml-100k.zip")

# Column names. The README inside the zip is the authority; these follow it.
RATING_COLS = ["user_id", "movie_id", "rating", "timestamp"]
GENRES = ["unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
          "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery",
          "Romance", "Sci-Fi", "Thriller", "War", "Western"]
MOVIE_COLS = ["movie_id", "title", "release_date", "video_release_date", "imdb_url"] + GENRES
USER_COLS = ["user_id", "age", "gender", "occupation", "zip_code"]

# What the README promises. Part 1 and Part 2 check the data against these.
README_COUNTS = {"ratings": 100_000, "users": 943, "movies": 1_682, "min_ratings_per_user": 20}


def download_if_missing() -> None:
    """Unzip the checked-in zip on first use; download only if it is missing."""
    if (ML_DIR / "u.data").exists():
        return
    DATA_DIR.mkdir(exist_ok=True)
    zip_path = ZIP_PATH if ZIP_PATH.exists() else DOWNLOADED_ZIP
    if not zip_path.exists():
        print(f"{ZIP_PATH.name} is not in the repo; downloading {ZIP_URL} ...")
        try:
            urllib.request.urlretrieve(ZIP_URL, zip_path)
        except Exception as e:  # noqa: BLE001 - we want the plain message
            sys.exit(
                f"Download failed: {e}\n"
                f"Either retry, set ML100K_URL to a mirror, or put ml-100k.zip in {REPO_ROOT}/ "
                f"and run this again."
            )
    print(f"Unzipping {zip_path.name} into {DATA_DIR}/ ...")
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(DATA_DIR)
    if not (ML_DIR / "u.data").exists():
        sys.exit(f"Unzipped, but {ML_DIR}/u.data is missing. Is this the right zip?")


def load_ratings() -> pd.DataFrame:
    """user_id, movie_id, rating (1-5 stars, integers), timestamp (unix seconds). Tab-separated."""
    download_if_missing()
    return pd.read_csv(ML_DIR / "u.data", sep="\t", header=None, names=RATING_COLS)


def load_movies() -> pd.DataFrame:
    """movie_id, title (with year), release_date, video_release_date, imdb_url, then 19 genre flags
    (1 = in that genre, 0 = not; a movie can carry several). Pipe-separated, latin-1 encoded:
    nine titles have accented characters, and reading this file as utf-8 fails."""
    download_if_missing()
    return pd.read_csv(ML_DIR / "u.item", sep="|", header=None, names=MOVIE_COLS, encoding="latin-1")


def load_users() -> pd.DataFrame:
    """user_id, age, gender (M/F), occupation, zip_code. Pipe-separated. Users are anonymous integers."""
    download_if_missing()
    return pd.read_csv(ML_DIR / "u.user", sep="|", header=None, names=USER_COLS, dtype={"zip_code": str})


def readme_text() -> str:
    download_if_missing()
    return (ML_DIR / "README").read_text(encoding="latin-1")


if __name__ == "__main__":
    # First, the repo itself: your work must live in your own repo, not in the template.
    sys.path.insert(0, str(REPO_ROOT))
    try:
        import sync_upstream
        kind, why = sync_upstream.origin_state()
    except Exception:  # noqa: BLE001
        kind, why = "ok", "?"
    if kind == "template":
        sys.exit("Repo check failed: " + why)
    if kind == "missing":
        print("Repo check: " + why + "\n")
    ratings, movies, users = load_ratings(), load_movies(), load_users()
    print(readme_text())
    print("=" * 72)
    print(f"ratings: {ratings.shape[0]:,} rows x {ratings.shape[1]} cols   (u.data)")
    print(f"movies:  {movies.shape[0]:,} rows x {movies.shape[1]} cols    (u.item)")
    print(f"users:   {users.shape[0]:,} rows x {users.shape[1]} cols      (u.user)")
    got = {
        "ratings": len(ratings),
        "users": ratings["user_id"].nunique(),
        "movies": movies["movie_id"].nunique(),
        "min_ratings_per_user": int(ratings.groupby("user_id").size().min()),
    }
    ok = True
    for k, want in README_COUNTS.items():
        mark = "OK " if got[k] == want else "MISMATCH"
        ok &= got[k] == want
        print(f"  {mark} {k}: README says {want:,}, data has {got[k]:,}")
    print("All README counts match." if ok else "Some counts do not match the README. Look into it before Part 1.")
    if kind == "ok":
        print(f"Repo check: origin is {why} (your own repo, not the template).")
