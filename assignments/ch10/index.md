# Ch. 10: Batman Movies — Functional Programming Lab

## Description

Keep the classic Batman movies context while practicing functional programming. Work with a small array of Batman movies and write pure functions that use `map`, `filter`, and `reduce` to transform and analyze data without mutating it.

## Learning Objectives

- Write pure functions whose outputs depend only on inputs.
- Use `map`, `filter`, and `reduce` to process arrays declaratively.
- Avoid mutations (treat inputs as read‑only) and return new values.
- Compose small functions for clarity and reuse.

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 10 - Batman Movies (FP)`.
- Use the JS panel only (no HTML/CSS).
- Open the CodePen Console (click `Console` at the bottom).
- Optional: Pen Settings → Behavior → enable “Clear Console on Run”.

## Dataset

Use this dataset in your Pen:

```js
/*********************************************
 * movieList DATASET
 *********************************************/
const movieList = [
  {
    title: "Batman",
    year: 1989,
    director: "Tim Burton",
    imdbRating: 7.5,
    metascore: 69,
    votes: 417000
  },
  {
    title: "Batman Returns",
    year: 1992,
    director: "Tim Burton",
    imdbRating: 7.1,
    metascore: 68,
    votes: 326000
  },
  {
    title: "Batman Forever",
    year: 1995,
    director: "Joel Schumacher",
    imdbRating: 5.4,
    metascore: 51,
    votes: 263000
  },
  {
    title: "Batman & Robin",
    year: 1997,
    director: "Joel Schumacher",
    imdbRating: 3.8,
    metascore: 29,
    votes: 234000
  },
  {
    title: "Batman Begins",
    year: 2005,
    director: "Christopher Nolan",
    imdbRating: 8.2,
    metascore: 70,
    votes: 1501000
  },
  {
    title: "The Dark Knight",
    year: 2008,
    director: "Christopher Nolan",
    imdbRating: 9.0,
    metascore: 84,
    votes: 2855058
  },
  {
    title: "The Dark Knight Rises",
    year: 2012,
    director: "Christopher Nolan",
    imdbRating: 8.4,
    metascore: 78,
    votes: 1760000
  },
  {
    title: "Batman v Superman: Dawn of Justice",
    year: 2016,
    director: "Zack Snyder",
    imdbRating: 6.4,
    metascore: 44,
    votes: 692000
  },
  {
    title: "The Lego Batman Movie",
    year: 2017,
    director: "Chris McKay",
    imdbRating: 7.3,
    metascore: 75,
    votes: 166000
  },
  {
    title: "The Batman",
    year: 2022,
    director: "Matt Reeves",
    imdbRating: 7.9,
    metascore: 72,
    votes: 656000
  }
];
```

## Tasks (Pure Functions)

Write each as a pure function that accepts `movieList` (or a derived list) as a parameter and returns a new value. Do not mutate inputs; create new arrays/values.

Core tasks
- `getTitles(movies)`: return an array of all titles.
- `getTitlesAfter(movies, year)`: return titles released strictly after `year` (e.g., 2000).
- `getUniqueDirectors(movies)`: return a unique list of directors.
- `countMovies(movies)`: return the number of movies.
- `getEarliest(movies)`: return the movie object with the smallest year.
- `getLatest(movies)`: return the movie object with the largest year.
- `getAverageRating(movies)`: return the average `imdbRating` (number).
- `getHighestRated(movies)`: return the movie object with the highest `imdbRating`.
- `getLowestRated(movies)`: return the movie object with the lowest `imdbRating`.
- `getAverageRatingByDirector(movies, director)`: average rating of that director’s movies (e.g., 'Christopher Nolan').
- `getMostProlificDirector(movies)`: return `{ director, count }` for the director with most movies.

Optional extensions
- With the provided fields `metascore` and `votes`, you can also add:
  - `getHighestBy(movies, key)` and `getLowestBy(movies, key)` to generalize min/max by any numeric key.
  - `getMostVoted(movies)`: movie with max votes.

## Displaying Results

In your main code, call these functions with `movieList` and `console.log()` the results. Keep logging outside the functions to preserve purity.

## Example Outputs

With the provided 10‑movie dataset:

```
Titles: Batman, Batman Returns, Batman Forever, Batman & Robin, Batman Begins, The Dark Knight, The Dark Knight Rises, Batman v Superman: Dawn of Justice, The Lego Batman Movie, The Batman
After 2000: Batman Begins, The Dark Knight, The Dark Knight Rises, Batman v Superman: Dawn of Justice, The Lego Batman Movie, The Batman
Directors: Tim Burton, Joel Schumacher, Christopher Nolan, Zack Snyder, Chris McKay, Matt Reeves
Count: 10
Earliest: Batman (1989)
Latest: The Batman (2022)
Average IMDB rating (all): 7.10
Highest rated: The Dark Knight (9.0)
Lowest rated: Batman & Robin (3.8)
Average IMDB rating (Christopher Nolan): 8.53
Most prolific director: Christopher Nolan (3)
```

## What to Submit

- The URL to your public CodePen `Ch. 10 - Batman Movies (FP)`.
- A note that core tasks run and print the expected checkpoints.

## Grading (25 pts)

- Pure function design (no mutations; parameters in, values out) (5)
- Titles, post‑2000, unique directors implemented with `map`/`filter` (8)
- Counts, earliest/latest, highest/lowest rating (8)
- Averages overall and by director (2)
- Clear console output and organization (2)

## Tips & Troubleshooting

- Floating point averages may have many decimals; use `toFixed(2)` when printing if you want rounded output.
- Guard against empty lists when averaging (e.g., return `0` or `NaN` explicitly if no movies match a filter).
- Use `console.log()` to verify intermediate arrays (e.g., filtered lists, mapped ratings) before reducing.
- Keep functions pure: do not mutate the `movieList` argument. Prefer `map`, `filter`, `reduce`, and spreading to create new arrays/values.
