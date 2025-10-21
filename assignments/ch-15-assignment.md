# Ch. 15 Assignment: Modify Page Structure — DOM Updates & Styles

## Description

Practice Chapter 15 by modifying the DOM after load: update text and attributes, add/remove/replace elements, insert at precise positions, and change styles (inline vs computed). You’ll implement small tasks in a single CodePen using the HTML and JS panels.

## Learning Objectives

- Update existing elements via `textContent`, `innerHTML`, `setAttribute`, and `classList`.
- Create elements with `document.createElement()` and text nodes via `document.createTextNode()`.
- Insert nodes using `appendChild()`, `insertBefore()`, and `insertAdjacentHTML()`.
- Replace and remove nodes with `replaceChild()` and `removeChild()`.
- Change styles with `element.style` and read styles with `getComputedStyle()`.
- Prefer batching DOM writes (create → set props → insert) to reduce reflows.

## Setup (CodePen)

- Create a new CodePen named `Ch. 15 - Modify Page Structure`.
- Use both the HTML and JS panels.
- Open the Console (bottom bar → `Console`).
- For each task, paste the provided HTML snippet into the HTML panel; write your JS in the JS panel.

## Instructions

Work top‑to‑bottom. Use `console.log()` for normal output and only use `innerHTML` for small snippets where asked; otherwise prefer `createElement()`.

1) Add a paragraph with a link (languages page)
- HTML snippet:

```html
<h3 class="beginning">Some languages</h3>
<div id="content">
  <ul id="languages">
    <li id="cpp">C++</li>
    <li id="java">Java</li>
    <li id="csharp">C#</li>
    <li id="php">PHP</li>
  </ul>
  <!-- Add a paragraph with a link below using JS -->
  <!-- Target URL: https://en.wikipedia.org/wiki/List_of_programming_languages -->
  
</div>
```

- JS: Create a `<p>` with an `<a>` child linking to the URL, then append it after the list.

```js
// 1) Add paragraph with link
const p = document.createElement('p');
const a = document.createElement('a');
a.href = 'https://en.wikipedia.org/wiki/List_of_programming_languages';
a.textContent = 'List of programming languages';
p.appendChild(a);
document.getElementById('content').appendChild(p);
```

2) Newspaper list (clickable links)
- Replace HTML with:

```html
<h3>Some newspapers</h3>
<div id="content"></div>
```

- JS: Given the array, render a clickable list into `#content` using `createElement()`.

```js
// 2) Newspaper list
const newspapers = [
  'https://www.nytimes.com',
  'https://www.washingtonpost.com',
  'http://www.economist.com'
];

const ul = document.createElement('ul');
newspapers.forEach(url => {
  const li = document.createElement('li');
  const link = document.createElement('a');
  link.href = url;
  link.textContent = url;
  link.target = '_blank';
  li.appendChild(link);
  ul.appendChild(li);
});
document.getElementById('content').appendChild(ul);
```

3) Mini‑dictionary (dl/dt/dd)
- Replace HTML with:

```html
<h3>A mini-dictionary</h3>
<div id="content"></div>
```

- JS: Build a `<dl>` where each `term` is a `<dt>` (with `<strong>`) and each `definition` is a `<dd>`.

```js
// 3) Mini-dictionary
const words = [
  { term: 'Procrastination', definition: 'Avoidance of doing a task that needs to be accomplished' },
  { term: 'Tautology', definition: 'logical argument constructed in such a way that it is logically irrefutable' },
  { term: 'Oxymoron', definition: 'figure of speech that juxtaposes elements that appear to be contradictory' }
];

const dl = document.createElement('dl');
words.forEach(({ term, definition }) => {
  const dt = document.createElement('dt');
  const strong = document.createElement('strong');
  strong.textContent = term;
  dt.appendChild(strong);
  const dd = document.createElement('dd');
  dd.textContent = definition;
  dl.appendChild(dt);
  dl.appendChild(dd);
});
document.getElementById('content').appendChild(dl);
```

4) Updating colors (ask user, apply styles)
- Replace HTML with any simple body content or reuse prior snippets.
- JS: Prompt for text color, then background color; update page styles.

```js
// 4) Updating colors
const textColor = prompt('Enter a text color (e.g., red or #ff0000):') || '';
const bgColor = prompt('Enter a background color (e.g., white or #ffffff):') || '';
if (textColor) document.body.style.color = textColor;
if (bgColor) document.body.style.backgroundColor = bgColor;
```

5) Information about an element (size list)
- Replace HTML with:

```html
<div id="content">ABC
  <br>Easy as
  <br>One, two, three
</div>
<div id="infos"></div>

<style>
#content {
  float: right;
  margin-top: 100px;
  margin-right: 50px;
}
</style>
```

- JS: Add a list to `#infos` showing the element’s width and height. Use `getComputedStyle()` for values.

```js
// 5) Info about #content dimensions
const box = document.getElementById('content');
const styles = getComputedStyle(box);
const width = styles.width;   // e.g., "300px"
const height = styles.height; // e.g., "120px"

const ulInfo = document.createElement('ul');
const liW = document.createElement('li');
liW.textContent = `Width: ${width}`;
const liH = document.createElement('li');
liH.textContent = `Height: ${height}`;
ulInfo.appendChild(liW);
ulInfo.appendChild(liH);
document.getElementById('infos').appendChild(ulInfo);
```

## Example Outputs

- Languages page: a paragraph appears below the list with a clickable link.
- Newspapers: a list of clickable links opens in a new tab.
- Mini‑dictionary: a `<dl>` with bold `<dt>` terms and `<dd>` definitions.
- Colors: page text/background update to the entered values.
- Info: `#infos` shows two list items for width and height (in px).

## What to Submit

- The URL to your public CodePen `Ch. 15 - Modify Page Structure`.
- A note that tasks 1–5 run with the provided HTML per section.

## Grading (10 pts)

- Paragraph + link creation using DOM APIs (2)
- Newspaper list: clickable links rendered from array (2)
- Mini‑dictionary with correct `<dl>/<dt>/<dd>` structure (2)
- Color prompts correctly update text and background (2)
- Element size list built using `getComputedStyle()` (2)

## Tips & Troubleshooting

- Prefer `createElement()` + property setting, then insert into DOM (batch changes).
- Reserve `innerHTML` for small, controlled snippets; avoid mixing with DOM nodes within the same container to prevent surprises.
- `element.style` only reflects inline styles; use `getComputedStyle()` to read final values.
- For precise measurements, `element.getBoundingClientRect()` also returns width/height in pixels.

