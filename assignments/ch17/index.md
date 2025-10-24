# Ch. 17: Forms Lab — Manipulate Forms

## Description

Practice Chapter 17 by handling form inputs in the browser: read and validate values, react to focus/blur/change/input events, prevent default submission, populate selects, and build a simple autocomplete. You’ll complete three tasks in a single CodePen using the HTML and JS panels.

## Learning Objectives

- Read/write input values via `.value` and control focus with `focus()`/`blur()`.
- Listen to `focus`, `blur`, `change`, `input`, and `submit` events.
- Prevent default submit with `e.preventDefault()` and show validation messages.
- Populate a `<select>` dynamically and react to selection changes.
- Implement basic autocomplete from a dataset.

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 17 - Forms Lab`.
- Use the HTML and JS panels (optional CSS panel for the autocomplete styles).
- Open the Console (bottom bar → `Console`) for any logs.
- Start from the Ch. 12 Personal Portfolio HTML. Add each form task inside a fresh `<section>` so your base layout remains intact while you extend it.

## Instructions

Work top‑to‑bottom. For each task, drop the provided markup into a new `<section>` on the page (keep existing sections) and write your JavaScript in the JS panel.

1) Password checker (submit validation)
- Create `<section id="ch17-password-checker">` with this form (note the `id` on the form):

```html
<section id="ch17-password-checker">
  <form id="password-form">
    <p>
      <label for="password1">Enter the password</label>:
      <input type="password" name="password1" id="password1" required>
    </p>
    <p>
      <label for="password2">Confirm the password</label>:
      <input type="password" name="password2" id="password2" required>
    </p>

    <input type="submit" value="Send">
  </form>

  <p id="passwordHelp"></p>
</section>
```

- JS: Validate on submit; rules: passwords equal, min length 6, at least one digit. Show a message in `#passwordHelp` and color it; prevent default submission in CodePen.

```js
// 1) Password checker
const form = document.getElementById('password-form');
const help = document.getElementById('passwordHelp');

form.addEventListener('submit', (e) => {
  const p1 = document.getElementById('password1').value;
  const p2 = document.getElementById('password2').value;
  const messages = [];

  if (p1 !== p2) messages.push('Passwords do not match.');
  if (p1.length < 6) messages.push('Password must be at least 6 characters.');
  if (!/\d/.test(p1)) messages.push('Password must contain at least one digit.');

  if (messages.length > 0) {
    help.textContent = messages.join(' ');
    help.style.color = 'red';
  } else {
    help.textContent = 'Password valid!';
    help.style.color = 'green';
  }
  e.preventDefault(); // Keep the page; don’t actually submit in CodePen
});
```

2) Character list (populate select and show characters)
- Add `<section id="ch17-characters">` with the following markup:

```html
<section id="ch17-characters">
  <h1>A few of the Game of Thrones characters</h1>
  <form>
    <label for="house">House</label>:
    <select name="house" id="house">
      <option value="" selected>Select a house</option>
    </select>
  </form>

  <ul id="characters"></ul>
</section>
```

- JS: Fill the house dropdown on load; update the character list when a house is selected.

```js
// 2) Character list
const houses = [
  { code: 'ST', name: 'Stark' },
  { code: 'LA', name: 'Lannister' },
  { code: 'BA', name: 'Baratheon' },
  { code: 'TA', name: 'Targaryen' }
];

const getCharacters = (houseCode) => {
  switch (houseCode) {
    case 'ST': return ['Eddard', 'Catelyn', 'Robb', 'Sansa', 'Arya', 'Jon Snow'];
    case 'LA': return ['Tywin', 'Cersei', 'Jaime', 'Tyrion'];
    case 'BA': return ['Robert', 'Stannis', 'Renly'];
    case 'TA': return ['Aerys', 'Daenerys', 'Viserys'];
    default: return [];
  }
};

const houseSelect = document.getElementById('house');
const charList = document.getElementById('characters');

// Populate houses
houses.forEach(h => {
  const opt = document.createElement('option');
  opt.value = h.code;
  opt.textContent = h.name;
  houseSelect.appendChild(opt);
});

// Update characters on selection
houseSelect.addEventListener('change', (e) => {
  const code = e.target.value;
  charList.innerHTML = '';
  getCharacters(code).forEach(name => {
    const li = document.createElement('li');
    li.textContent = name;
    charList.appendChild(li);
  });
});
```

3) Autocomplete (countries starting with “A”)
- Insert `<section id="ch17-autocomplete">` with the input, suggestion area, and inline styles:

```html
<section id="ch17-autocomplete">
  <label for="country">Enter a country name</label>:
  <input type="text" id="country">
  <div id="suggestions"></div>

  <style>
    /* Add spacing between each country suggestion */
    .suggestion { padding-left: 2px; padding-right: 2px; }
    /* Change suggestion color when hovering it with the mouse */
    .suggestion:hover { background-color: #adf; cursor: pointer; }
    /* Position the suggestion list just below the input box */
    #suggestions { position: absolute; border: 1px solid black; left: 155px; }
  </style>
</section>
```

- JS: As the user types, show matching countries below; clicking a suggestion fills the input and clears suggestions.

```js
// 3) Autocomplete
const countryList = [
  'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Anguilla', 'Antarctica',
  'Antigua-and-Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Autria', 'Azerbaïjan'
];

const input = document.getElementById('country');
const sugg = document.getElementById('suggestions');

const clearSuggestions = () => { sugg.innerHTML = ''; };

input.addEventListener('input', () => {
  const q = input.value.trim().toLowerCase();
  clearSuggestions();
  if (!q) return;
  // Show countries that start with the typed prefix (case-insensitive)
  countryList
    .filter(name => name.toLowerCase().startsWith(q))
    .forEach(name => {
      const div = document.createElement('div');
      div.className = 'suggestion';
      div.textContent = name;
      div.addEventListener('click', () => {
        input.value = name;
        clearSuggestions();
      });
      sugg.appendChild(div);
    });
});

// Optional: hide suggestions when leaving the input
input.addEventListener('blur', () => {
  // Give a small delay so click can register before clearing
  setTimeout(clearSuggestions, 150);
});
```

## Example Outputs

- Password checker: invalid rules show red message; valid shows green message; submit is prevented in CodePen.
- Character list: houses populate on load; selecting one lists its characters.
- Autocomplete: typing “Ar” shows items like “Argentina”, clicking a suggestion fills the input and hides the list.

## What to Submit

- The URL to your public CodePen `Ch. 17 - Forms Lab`.
- A short note that tasks 1–3 run and behave as described.

## Grading (25 pts)

- Password validation on submit (messages + color, prevent default) (10)
- House select populated and character list updates on change (7)
- Autocomplete shows filtered suggestions and fills on click (8)

## Tips & Troubleshooting

- Use `e.preventDefault()` in submit handlers when you want to stop navigation.
- `focus`/`blur` are useful for showing inline help; `input` is best for live validation.
- Consider trimming input with `.trim()`; compare case-insensitively with `.toLowerCase()`.
