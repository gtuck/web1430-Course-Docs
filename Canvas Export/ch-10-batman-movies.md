**Objective**
Strengthen your functional programming skills by working with a curated dataset of Batman movies. You will apply higher-order functions (e.g., `map`, `filter`, and `reduce`) and write pure functions to transform and analyze data—while adhering to functional programming principles of immutability and no side effects.

---

### Part 1: Set Up Your Project

1. **Create a new CodePen** and name it **"Batman Movies"**.
2. **Add the Dataset**: 

  - Start with the classic `movieList` dataset from *The JS Way*, then update it with additional Batman theatrical films from the official Batman Theatrical Films list ([https://www.imdb.com/list/ls538854829/?sort=release_date%2Casc](https://www.imdb.com/list/ls538854829/?sort=release_date%2Casc)).
  - Ensure each movie object contains these properties: 

```
{
  title: "Batman",
  year: 1989,
  director: "Tim Burton",
  imdbRating: 7.5,
  metascore: 69,
  votes: 417000
}
```

    - `title` - string (title of the movie)
    - `year` - number (year released)
    - `director` - string (director's name)
    - `imdbRating` - number (IMDB rating)
    - `metascore` - number (Metascore from metacritic.com)
    - `votes` - number (IMDB votes in numeric form, e.g. 417K → 417000)

---

### Part 2: Functional Programming Tasks

Write **pure functions** to accomplish each of the following tasks. A function is pure if it:

- Receives all necessary data via parameters.
- Returns a value based on its input (with no hidden side effects).
- Does not mutate or depend on external state.

Additional requirements:

- Create clearly named functions (e.g., getAllBatmanTitles).
- Inside the function, use higher-order functions (map, filter, reduce) to operate on the data.
- Return your results from the function, rather than logging them directly to the console.

### Task list:

1. **All Titles - **Return an array of **all Batman movie titles** in the dataset.

2. **Post-2000 Releases - **Return an array of **Batman movie titles released after the year 2000**.

3. **Directors - **Return a unique list of all **Batman movie directors**.

4. **Total Movie Count - **Return the total **number of Batman movies** in the dataset.

5. **Earliest Release - **Return the **earliest-released** Batman movie (the one with the smallest year).

6. **Most Recent Release - **Return the **most recent** Batman movie (the one with the largest year).

7. **Most Prolific Director - **Return the name of the **director who has made the most Batman movies**, along with the count.

8. **Highest Metascore - **Return the **Batman movie with the highest Metascore**, along with the score.

9. **Lowest Metascore - **Return the **Batman movie with the lowest Metascore**, along with the score.

10. **Average IMDB Rating - **Return the **average IMDB rating** for all Batman movies.

11. **Highest IMDB Rating - **Return the **Batman movie with the highest IMDB rating**, along with its rating.

12. **Lowest IMDB Rating - **Return the **Batman movie with the lowest IMDB rating**, along with its rating.

13. **Average IMDB Rating (Christopher Nolan) - **Return the **average IMDB rating of all Batman movies directed by Christopher Nolan**.

14. **Most IMDB Votes - **Return the **Batman movie with the greatest number of IMDB votes**, along with that vote count.

---

### Part 3: Displaying Your Results

Once you have written the pure functions, you can:

- **Invoke** each function, passing the dataset as an argument.
- **Log the results** to the console.

**Example Output:**

```
1. Batman movie titles: Batman, Batman Returns, Batman Forever, Batman & Robin, Batman Begins, The Dark Knight, The Dark Knight Rises, Batman v Superman: Dawn of Justice, The Lego Batman Movie, The Batman
2. Batman movies made after 2000: Batman Begins, The Dark Knight, The Dark Knight Rises, Batman v Superman: Dawn of Justice, The Lego Batman Movie, The Batman
3. Batman movie directors: Tim Burton, Joel Schumacher, Christopher Nolan, Zack Snyder, Chris McKay, Matt Reeves
4. 10 Batman movies have been made.
5. The first Batman movie released was 'Batman' in 1989.
6. The most recent Batman movie is 'The Batman', released in 2022.
7. Christopher Nolan has directed the most Batman movies with 3 movies.
8. 'The Dark Knight' has the highest metascore of 84.
9. 'Batman & Robin' has the lowest metascore of 29.
10. The average IMDB rating for all Batman movies is 7.10.
11. 'The Dark Knight' has the highest IMDB rating of 9.
12. 'Batman & Robin' has the lowest IMDB rating of 3.8.
13. Christopher Nolan's Batman movies have an average IMDB rating of 8.53.
14. 'The Dark Knight' has received the most IMDB votes, with 2855058 votes.
```

---

### Part 4: Submission

1. **Ensure your CodePen** is saved and titled appropriately.
2. **Submit the URL** to your CodePen.
