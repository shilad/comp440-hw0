"""
Part 4: your own question, answered with one plot.

    uv run python part4.py

Write the question on the `**Question:**` line of WRITEUP.md first. A menu, or bring your own:
does a movie's mean rating change with how many people rated it; do heavy raters rate
differently from light ones; how did average ratings drift over the seven months; do genres
differ in how much people disagree.

Then this file draws one plot, not a table, with labeled axes and a title, and saves it to
figures/part4.png; and its check() recomputes one plotted number by a different route (a
hand-filtered slice, a different pandas path, a manual count on a small subset) and prints
MATCH or MISMATCH with both values. WRITEUP.md names the function that printed any number you
quote and says what check() recomputed and which word it printed. Put a `# Claude:` comment
above any function Claude wrote.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # draw to a file, never a window
import matplotlib.pyplot as plt

from load_data import load_movies, load_ratings, load_users

ratings = load_ratings()   # user_id, movie_id, rating, timestamp
movies = load_movies()     # movie_id, title, release_date, video_release_date, imdb_url, 19 genre flags
users = load_users()       # user_id, age, gender, occupation, zip_code

FIGURE = Path(__file__).resolve().parent / "figures" / "part4.png"


def plot():
    """The one plot that answers the question; saves FIGURE."""
    fig, ax = plt.subplots()
    # draw on ax here, then label it
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")
    if not ax.has_data():
        print("plot(): not written yet")
        return
    FIGURE.parent.mkdir(exist_ok=True)
    fig.savefig(FIGURE, dpi=150, bbox_inches="tight")
    print(f"saved figures/{FIGURE.name}")


def check():
    """One plotted number, recomputed by a different route. Prints MATCH or MISMATCH with both."""
    plotted = None      # the value as the plot computed it
    recomputed = None   # the same value by another route
    if plotted is None or recomputed is None:
        print("check(): not written yet")
        return
    word = "MATCH" if plotted == recomputed else "MISMATCH"
    print(f"check(): plotted = {plotted}, recomputed = {recomputed} -> {word}")


if __name__ == "__main__":
    plot()
    check()
