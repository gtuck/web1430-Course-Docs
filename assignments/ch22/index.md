# Ch. 22: Use Web APIs — Fetch Real Data

## Description

Practice Chapter 22 by consuming real web APIs with `fetch()`: parse JSON, render results, handle errors, and build simple UI interactions. You’ll implement three tasks in one CodePen.

## Learning Objectives

- Call open web APIs over HTTPS with `fetch()`.
- Parse responses as JSON and read nested fields.
- Handle errors (`response.ok`, 404) and network failures via `catch`.
- Update the DOM with fetched data and clear prior results as needed.
- Wire basic UI to trigger API calls (buttons, inputs, links).

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 22 - Use Web APIs`.
- Use HTML and JS panels (optional CSS for light styling).
- Open the Console (bottom bar → `Console`).
- Begin with the Ch. 12 Personal Portfolio HTML. Add each API task inside a dedicated `<section>` so your portfolio layout persists.

## Instructions

Work top‑to‑bottom. For each section, insert the HTML inside a new `<section>` on your existing page and write the JS in the JS panel.

1) Star Wars planets (SWAPI)
- Insert `<section id="ch22-planets">` with link and info containers:

```html
<section id="ch22-planets">
  <h2>Some Star Wars planets</h2>
  <div id="links"></div>
  <div id="infos"></div>
</section>
```

- JS: Generate links for planet IDs 1–10. Clicking a link fetches `https://swapi.dev/api/planets/{id}/` and displays name, climate, terrain, and population. Prevent default link navigation.

```js
// 1) SWAPI planets 1..10
const links = document.getElementById('links');
const info = document.getElementById('infos');

for (let id = 1; id <= 10; id++) {
  const a = document.createElement('a');
  a.href = '#';
  a.textContent = `Planet ${id}`;
  a.style.marginRight = '8px';
  a.addEventListener('click', (e) => {
    e.preventDefault();
    info.textContent = 'Loading...';
    fetch(`https://swapi.dev/api/planets/${id}/`)
      .then(r => {
        if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
        return r.json();
      })
      .then(p => {
        info.innerHTML = '';
        const title = document.createElement('h3');
        title.textContent = p.name;
        const details = document.createElement('p');
        details.textContent = `Climate: ${p.climate} · Terrain: ${p.terrain} · Population: ${p.population}`;
        info.append(title, details);
      })
      .catch(err => {
        info.textContent = `Failed to load planet ${id}: ${err.message}`;
      });
  });
  links.appendChild(a);
}
```

## Example Behaviors

- SWAPI: Links Planet 1..10 fetch and display details for each planet.

## What to Submit

- The URL to your public CodePen `Ch. 22 - Use Web APIs`.
- A short note that all three sections work and errors are handled gracefully.

## Grading (25 pts)

- SWAPI planets: generated links and detail fetch (8)
- Clean DOM updates and basic error handling (1)

## Tips & Troubleshooting

- Always use `https` URLs in the browser to avoid mixed‑content blocks.
- Check `response.ok` and throw to route failures into `.catch()`.
- Some APIs rate‑limit; retry later if you see a 429 or similar.
- Network calls are asynchronous; keep rendering inside `then()`.
- Use `console.log()` to inspect intermediate values (responses, parsed JSON) when debugging.
