# The data, described for Claude

This is what the cold Claude gets, verbatim, at the top of every question `cold_session.py`
asks (run `uv run python cold_session.py --show-prompt best` to see the whole prompt). It says
what the files are and where they live. It does not say how many rows they have: counting is
part of the work. Do not edit it; every student and the Reference Analyst ask the same question.

```
The MovieLens 100K dataset from GroupLens is in data/ml-100k/ (relative to the
current working directory). Three files matter:

- u.data: one rating per line, tab-separated: user id | movie id | rating (1 to 5
  stars, integers) | timestamp (unix seconds).
- u.item: one movie per line, pipe-separated, latin-1 encoded: movie id | title
  (with year) | release date | video release date | IMDb URL | then 19 genre flags in
  this order: unknown, Action, Adventure, Animation, Children's, Comedy, Crime,
  Documentary, Drama, Fantasy, Film-Noir, Horror, Musical, Mystery, Romance, Sci-Fi,
  Thriller, War, Western (1 = the movie is in that genre, 0 = it is not; a movie can
  be in several).
- u.user: one user per line, pipe-separated: user id | age | gender | occupation |
  zip code.

Neither file has a header row. I can run Python 3 with pandas, numpy, and matplotlib.
You cannot run code or read files in this conversation; answer in text, and include
any code you would want me to run.
```
