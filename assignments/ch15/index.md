# Ch. 15: Modify Page Structure — DOM Updates & Styles

## Description

Practice Chapter 15 by modifying the DOM after load: update text and attributes, add/remove/replace elements, insert at precise positions, and change styles (inline vs computed). You’ll implement small tasks in a single CodePen using the HTML and JS panels.

## Learning Objectives

- Update existing elements via `textContent`, `innerHTML`, `setAttribute`, and `classList`.
- Create elements with `document.createElement()` and text nodes via `document.createTextNode()`.
- Insert nodes using `appendChild()`, `insertBefore()`, and `insertAdjacentHTML()`.
- Replace and remove nodes with `replaceChild()` and `removeChild()`.
- Change styles with `element.style` and read styles with `getComputedStyle()`.
- Prefer batching DOM writes (create → set props → insert) to reduce reflows.

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 15 - Modify Page Structure`.
- Use both the HTML and JS panels.
- Open the Console (bottom bar → `Console`).
- Start the HTML panel with the Ch. 12 Personal Portfolio base structure (header, `<section>` blocks, footer). For each task below, extend that same page. Add new semantic `<section>` elements that follow the portfolio’s style rather than replacing the whole document. If a section needs a list or other structure that isn’t present yet, add it before writing the JavaScript.

## Instructions

Work top‑to‑bottom. Use `console.log()` for normal output and only use `innerHTML` for small snippets where asked; otherwise prefer `createElement()`. Each task should live in its own `<section>` so the page stays organized.

1) Add a paragraph with a link (languages section)
- In a new `<section id="ch15-languages">`, mirror the structure below. Use a unique container ID so the JavaScript can target it.

```html
<section id="ch15-languages">
  <h3 class="beginning">Some languages</h3>
  <div id="languages-content">
    <ul id="languages">
      <li id="cpp">C++</li>
      <li id="java">Java</li>
      <li id="csharp">C#</li>
      <li id="php">PHP</li>
    </ul>
    <!-- Add a paragraph with a link below using JS -->
    <!-- Target URL: https://en.wikipedia.org/wiki/List_of_programming_languages -->
    
  </div>
</section>
```

- JS: Create a `<p>` with an `<a>` child linking to the URL, then append it after the list inside `#languages-content`.

```js
// 1) Add paragraph with link
const languageContainer = document.getElementById('languages-content');
const p = document.createElement('p');
const a = document.createElement('a');
a.href = 'https://en.wikipedia.org/wiki/List_of_programming_languages';
a.textContent = 'List of programming languages';
p.appendChild(a);
languageContainer.appendChild(p);
```

2) Newspaper list (clickable links)
- In another `<section id="ch15-newspapers">`, add the following markup so you have a container ready for the generated list:

```html
<section id="ch15-newspapers">
  <h3>Some newspapers</h3>
  <div id="newspapers-content"></div>
</section>
```

- JS: Given the array, render a clickable list into `#newspapers-content` using `createElement()`.

```js
// 2) Newspaper list
const newspapersContainer = document.getElementById('newspapers-content');
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
newspapersContainer.appendChild(ul);
```

3) Mini‑dictionary (dl/dt/dd)
- Add a `<section id="ch15-dictionary">` that looks like this:

```html
<section id="ch15-dictionary">
  <h3>A mini-dictionary</h3>
  <div id="dictionary-content"></div>
</section>
```

- JS: Build a `<dl>` where each `term` is a `<dt>` (with `<strong>`) and each `definition` is a `<dd>`, and append it to `#dictionary-content`.

```js
// 3) Mini-dictionary
const dictionaryContainer = document.getElementById('dictionary-content');
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
dictionaryContainer.appendChild(dl);
```

4) Updating colors (ask user, apply styles)
- Reuse the existing page content from your earlier sections. No extra HTML is required—your prompts will target `document.body`.
- JS: Prompt for text color, then background color; update page styles.

```js
// 4) Updating colors
const textColor = prompt('Enter a text color (e.g., red or #ff0000):') || '';
const bgColor = prompt('Enter a background color (e.g., white or #ffffff):') || '';
if (textColor) document.body.style.color = textColor;
if (bgColor) document.body.style.backgroundColor = bgColor;
```

5) Information about an element (size list)
- Add another section (for example `<section id="ch15-dimensions">`) that includes both the content box and an info container. Keep the inline styles inside a `<style>` block in that section.

```html
<section id="ch15-dimensions">
  <div id="dimension-content">ABC
    <br>Easy as
    <br>One, two, three
  </div>
  <div id="dimension-infos"></div>

  <style>
    #dimension-content {
      float: right;
      margin-top: 100px;
      margin-right: 50px;
    }
  </style>
</section>
```

- JS: Add a list to `#dimension-infos` showing the element’s width and height. Use `getComputedStyle()` for values.

```js
// 5) Info about #dimension-content dimensions
const box = document.getElementById('dimension-content');
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
document.getElementById('dimension-infos').appendChild(ulInfo);
```

## Example Outputs

- Languages page: a paragraph appears below the list with a clickable link.
- Newspapers: a list of clickable links opens in a new tab.
- Mini‑dictionary: a `<dl>` with bold `<dt>` terms and `<dd>` definitions.
- Colors: page text/background update to the entered values.
- Info: `#dimension-infos` shows two list items for width and height (in px).

## What to Submit

- The URL to your public CodePen `Ch. 15 - Modify Page Structure`.
- A note that tasks 1–5 run with the provided HTML per section.

## Grading (25 pts)

- Paragraph + link creation using DOM APIs (5)
- Newspaper list: clickable links rendered from array (5)
- Mini‑dictionary with correct `<dl>/<dt>/<dd>` structure (5)
- Color prompts correctly update text and background (5)
- Element size list built using `getComputedStyle()` (5)

## Tips & Troubleshooting

- Prefer `createElement()` + property setting, then insert into DOM (batch changes).
- Reserve `innerHTML` for small, controlled snippets; avoid mixing with DOM nodes within the same container to prevent surprises.
- `element.style` only reflects inline styles; use `getComputedStyle()` to read final values.
- For precise measurements, `element.getBoundingClientRect()` also returns width/height in pixels.
