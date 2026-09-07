# The data files

What the three MovieLens files hold. `load_data.py` reads all three.

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

None of the three files has a header row.
```
