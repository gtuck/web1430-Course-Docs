# Ch. 21: Query a Web Server — fetch + JSON

## Description

Practice Chapter 21 by fetching remote resources asynchronously with `fetch()`, working with promises, reading response bodies as text and JSON, handling errors, and rendering results into the DOM.

## Learning Objectives

- Send asynchronous HTTP requests with `fetch(url)`.
- Work with promises using `then()` and `catch()`.
- Read response bodies via `response.text()` and `response.json()`.
- Handle network and parsing errors gracefully.
- Render fetched data to the page using DOM methods.

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 21 - Query a Web Server`.
- Use HTML and JS panels (no build tools required).
- Open the Console (bottom bar → `Console`) for debugging.
- Start from your Ch. 12 Personal Portfolio HTML. Add the fetch lab content as new `<section>` blocks so the page retains its semantic structure.

## Instructions

Add a new `<section id="ch21-fetch">` to your page that contains the elements you’ll populate with fetch results:

```html
<section id="ch21-fetch">
  <h2>A few programming languages</h2>
  <ul id="languageList"></ul>

  <h2>Some famous paintings</h2>
  <table id="paintings">
    <tr>
      <th>Name</th>
      <th>Year</th>
      <th>Artist</th>
    </tr>
    <!-- rows will be appended here by JS -->
    
  </table>
</section>
```

1) Language list (fetch text)
- Fetch the semicolon‑separated file and render each language as an `<li>` under `#languageList`.
- URL:
  - https://raw.githubusercontent.com/bpesquet/thejsway/master/resources/languages.txt

```js
// 1) Fetch text, split by ';', render as list items
const langUrl = 'https://raw.githubusercontent.com/bpesquet/thejsway/master/resources/languages.txt';
const langList = document.getElementById('languageList');

fetch(langUrl)
  .then(response => response.text())
  .then(text => {
    // Example text: "C++;Java;C#;PHP"
    text.split(';').forEach(name => {
      const li = document.createElement('li');
      li.textContent = name;
      langList.appendChild(li);
    });
  })
  .catch(err => {
    console.error('Languages fetch failed:', err.message);
  });
```

2) Famous paintings (fetch JSON)
- Fetch the JSON array and append one `<tr>` per painting with three `<td>` cells: name, year, artist.
- URL:
  - https://raw.githubusercontent.com/bpesquet/thejsway/master/resources/paintings.json

```js
// 2) Fetch JSON, render table rows
const paintingsUrl = 'https://raw.githubusercontent.com/bpesquet/thejsway/master/resources/paintings.json';
const table = document.getElementById('paintings');

fetch(paintingsUrl)
  .then(response => response.json())
  .then(paintings => {
    paintings.forEach(p => {
      const tr = document.createElement('tr');
      const tdName = document.createElement('td');
      const tdYear = document.createElement('td');
      const tdArtist = document.createElement('td');
      tdName.textContent = p.name;
      tdYear.textContent = p.year;
      tdArtist.textContent = p.artist;
      tr.append(tdName, tdYear, tdArtist);
      table.appendChild(tr);
    });
  })
  .catch(err => {
    console.error('Paintings fetch failed:', err.message);
  });
```

## Example Outputs

- Language list shows 4 items: C++, Java, C#, PHP.
- Paintings table shows 3 rows: The Starry Night (1889, Vincent Van Gogh), The Scream (1893, Edvard Munch), Guernica (1937, Pablo Picasso).

## What to Submit

- The URL to your public CodePen `Ch. 21 - Query a Web Server`.
- A note that both sections render successfully and errors (if any) are logged.

## Grading (25 pts)

- Uses `fetch()` with proper `then()`/`catch()` for both requests (8)
- Text fetch: splits by `;` and renders `<li>` items (5)
- JSON fetch: appends table rows with name/year/artist (8)
- Clean DOM rendering and basic error handling (4)

## Tips & Troubleshooting

- Always use `https` URLs to avoid mixed‑content issues in the browser.
- The returned `Response` may be ok/!ok; for robust handling, you can check `if (!response.ok) throw new Error(response.statusText)` before parsing.
- Network calls are asynchronous; keep DOM rendering inside the `then()` callbacks.
- If nothing appears, check the Console for errors (CORS, typos, parse errors).
- Use `console.log()` to verify intermediate values (e.g., raw response, parsed text/JSON) when debugging.
