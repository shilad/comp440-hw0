"""
Claude's answers to the three questions in questions.md.

    uv run python claude_answers_1_2_3.py

Filled in by a Claude that has never seen the student's work. Kept as it was written.
"""

from load_data import load_all


def claude_answers():
    print("claude's answers unimplemented")  # delete this line when you start
    ratings, ratings_df, movies, movies_df, users, users_df = load_all()


if __name__ == "__main__":
    claude_answers()
