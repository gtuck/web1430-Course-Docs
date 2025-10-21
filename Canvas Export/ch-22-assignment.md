# Ch. 22 Assignment: Use Web APIs — Fetch Real Data

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

## Instructions

Work top‑to‑bottom. For each section, place the snippet in the HTML panel and write the JS in the JS panel.

1) More beer please (Punk API)
- HTML:

```html
<button id="grabButton">Grab a beer</button>
<div id="beer"></div>
```

- JS: On click, fetch a random beer and display name, description, ABV, volume (with units), and first_brewed. Clear previous result before rendering.

```js
// 1) Punk API — random beer with extra fields
const beerBox = document.getElementById('beer');
const grabRandomBeer = () => {
  fetch('https://api.punkapi.com/v2/beers/random')
    .then(r => r.json())
    .then(beers => {
      const beer = beers[0];
      beerBox.innerHTML = '';
      const nameEl = document.createElement('h2');
      nameEl.textContent = beer.name;
      const descEl = document.createElement('p');
      descEl.textContent = beer.description;
      const metaEl = document.createElement('p');
      metaEl.textContent = `ABV: ${beer.abv}% · Volume: ${beer.volume.value} ${beer.volume.unit} · First brewed: ${beer.first_brewed}`;
      beerBox.append(nameEl, descEl, metaEl);
    })
    .catch(err => {
      console.error('Beer fetch failed:', err.message);
    });
};
document.getElementById('grabButton').addEventListener('click', grabRandomBeer);
```

2) GitHub profile lookup (GitHub Users API)
- HTML:

```html
<h2>GitHub Profile</h2>
<input id="login" type="text" placeholder="Enter GitHub login" />
<button id="loadProfile">Load Profile</button>
<div id="profile"></div>
```

- JS: On click, fetch `https://api.github.com/users/{login}`. Show avatar, name (or login), and website/blog link if present. Handle 404 with a friendly message.

```js
// 2) GitHub user profile
const profileBox = document.getElementById('profile');
document.getElementById('loadProfile').addEventListener('click', () => {
  const login = (document.getElementById('login').value || '').trim();
  profileBox.innerHTML = '';
  if (!login) return;
  fetch(`https://api.github.com/users/${encodeURIComponent(login)}`)
    .then(r => {
      if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
      return r.json();
    })
    .then(user => {
      const img = document.createElement('img');
      img.src = user.avatar_url;
      img.alt = `${user.login} avatar`;
      img.width = 100;
      const name = document.createElement('h3');
      name.textContent = user.name || user.login;
      const site = document.createElement('p');
      const blog = user.blog && user.blog.trim();
      if (blog) {
        const a = document.createElement('a');
        a.href = blog.startsWith('http') ? blog : `https://${blog}`;
        a.textContent = a.href;
        a.target = '_blank';
        site.append('Website: ', a);
      } else {
        site.textContent = 'Website: (none)';
      }
      profileBox.append(img, name, site);
    })
    .catch(err => {
      const msg = document.createElement('p');
      msg.style.color = 'red';
      msg.textContent = `Could not load user "${login}": ${err.message}`;
      profileBox.appendChild(msg);
    });
});
```

3) Star Wars planets (SWAPI)
- HTML:

```html
<h2>Some Star Wars planets</h2>
<div id="links"></div>
<div id="infos"></div>
```

- JS: Generate links for planet IDs 1–10. Clicking a link fetches `https://swapi.dev/api/planets/{id}/` and displays name, climate, terrain, and population. Prevent default link navigation.

```js
// 3) SWAPI planets 1..10
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

- Punk API: Clicking “Grab a beer” shows name, description, ABV, volume, and first brewed.
- GitHub: Enter a login (e.g., `brendaneich`) and show avatar, name, and website (if provided). A 404 shows a red error message.
- SWAPI: Links Planet 1..10 fetch and display details for each planet.

## What to Submit

- The URL to your public CodePen `Ch. 22 - Use Web APIs`.
- A short note that all three sections work and errors are handled gracefully.

## Grading (10 pts)

- Punk API: fetch + render extended fields (3)
- GitHub profile: fetch by login with 404 handling (3)
- SWAPI planets: generated links and detail fetch (3)
- Clean DOM updates and basic error handling (1)

## Tips & Troubleshooting

- Always use `https` URLs in the browser to avoid mixed‑content blocks.
- Check `response.ok` and throw to route failures into `.catch()`.
- Some APIs rate‑limit; retry later if you see a 429 or similar.
- Network calls are asynchronous; keep rendering inside `then()`.

