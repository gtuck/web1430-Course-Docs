# Ch. 16 Assignment: React to Events — Interactive Page Lab

## Description

Practice Chapter 16 by wiring event listeners, handling keyboard and mouse events, preventing defaults, and updating the DOM in response to user actions. You’ll implement four small interactive tasks in one CodePen.

## Learning Objectives

- Attach/detach listeners with `addEventListener` / `removeEventListener`.
- Read `Event` properties (`type`, `target`, `key`, `button`, `clientX/Y`).
- Handle keyboard (`keydown`/`keyup`) and mouse (`click`, `mousedown`, `mouseup`) events.
- Prevent default behavior with `e.preventDefault()` and manage simple propagation as needed.
- Update the DOM in response to events.

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 16 - React to Events`.
- Use both the HTML and JS panels.
- Open the Console (bottom bar → `Console`).

## Instructions

Work top‑to‑bottom. For each section, place the snippet in the HTML panel (replacing the prior one unless noted) and write the JS in the JS panel.

1) Counting clicks (with deactivate)
- HTML:

```html
<button id="myButton">Click me!</button>
<p>You clicked on the button <span id="clickCount">0</span> times</p>
<button id="deactivate">Deactivate counting</button>
```

- JS: Increment count on `#myButton` clicks; `#deactivate` stops counting.

```js
// 1) Counting clicks
const myButton = document.getElementById('myButton');
const deactivate = document.getElementById('deactivate');
const countSpan = document.getElementById('clickCount');

let count = 0;
const increment = () => {
  count += 1;
  countSpan.textContent = String(count);
};

myButton.addEventListener('click', increment);

deactivate.addEventListener('click', () => {
  myButton.removeEventListener('click', increment);
});
```

2) Changing colors by key (R, Y, G, B)
- HTML:

```html
<p>Press the R (red), Y (yellow), G (green) or B (blue) key to change paragraph colors accordingly.</p>

<h1>Paragraph 1</h1>
<div>…content…</div>

<h1>Paragraph 2</h1>
<div>…content…</div>

<h1>Paragraph 3</h1>
<div>…content…</div>
```

- JS: On keyup, set background color for all `div` elements based on key pressed.

```js
// 2) Changing colors
const setDivBg = (color) => {
  document.querySelectorAll('div').forEach(d => {
    d.style.backgroundColor = color;
  });
};

document.addEventListener('keyup', (e) => {
  const k = (e.key || '').toLowerCase();
  if (k === 'r') setDivBg('red');
  else if (k === 'y') setDivBg('yellow');
  else if (k === 'g') setDivBg('lightgreen');
  else if (k === 'b') setDivBg('lightblue');
});
```

3) Dessert list (add and rename on click)
- HTML:

```html
<h1>My favourite desserts</h1>
<ul id="desserts"></ul>
<button id="addButton">Add a dessert</button>
```

- JS: On “Add a dessert”, prompt for a name and append a new `<li>` with that name. Bonus: clicking an `<li>` prompts to rename it.

```js
// 3) Dessert list
const list = document.getElementById('desserts');
const addBtn = document.getElementById('addButton');

function makeItem(name) {
  const li = document.createElement('li');
  li.textContent = name;
  li.tabIndex = 0; // focusable for accessibility
  li.addEventListener('click', () => {
    const next = prompt('Rename dessert:', li.textContent);
    if (next && next.trim()) li.textContent = next.trim();
  });
  return li;
}

addBtn.addEventListener('click', () => {
  const name = prompt('Enter a dessert name:');
  if (name && name.trim()) list.appendChild(makeItem(name.trim()));
});
```

4) Interactive quiz (show answers per question)
- HTML:

```html
<div id="content"></div>
```

- JS: Render each question with a “Show the answer” button that reveals the answer (and replaces the button) when clicked.

```js
// 4) Interactive quiz
const questions = [
  { statement: '2+2?', answer: '2+2 = 4' },
  { statement: 'In which year did Christopher Columbus discover America?', answer: '1492' },
  { statement: 'What occurs twice in a lifetime, but once in every year, twice in a week but never in a day?', answer: 'The E letter' }
];

const container = document.getElementById('content');

questions.forEach(q => {
  const wrapper = document.createElement('div');
  const p = document.createElement('p');
  p.textContent = q.statement;
  const btn = document.createElement('button');
  btn.textContent = 'Show the answer';
  btn.addEventListener('click', () => {
    const ans = document.createElement('p');
    ans.textContent = q.answer;
    wrapper.replaceChild(ans, btn);
  });
  wrapper.appendChild(p);
  wrapper.appendChild(btn);
  container.appendChild(wrapper);
});
```

## Example Outputs

- Click counter increments until “Deactivate counting” disables it.
- Pressing R/Y/G/B changes all `div` backgrounds accordingly.
- “Add a dessert” appends a new list item; clicking an item prompts a rename.
- Quiz shows each question with a button; clicking reveals the answer for that question only.

## What to Submit

- The URL to your public CodePen `Ch. 16 - React to Events`.
- A short note that tasks 1–4 run and behave as described.

## Grading (25 pts)

- Click counter with deactivate using `removeEventListener` (5)
- Keyboard color changes on R/Y/G/B for all `div`s (5)
- Dessert list: add via prompt, rename on click (7)
- Quiz renders from data and reveals individual answers (8)

## Tips & Troubleshooting

- Keep references to named handlers if you plan to remove them later.
- Prefer updating only what changed in the DOM for responsiveness.
- Use `e.preventDefault()` for links/forms when you need to stop navigation/submission.
- Consider `e.stopPropagation()` when parent handlers fire unintentionally.
