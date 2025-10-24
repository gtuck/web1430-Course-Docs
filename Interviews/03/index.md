# Interview 03 Script — Chapters 16–22 (5 minutes)

- Duration: 5 minutes on Zoom (screen-share required)
- Scope: Ch. 16 (events), Ch. 17 (forms + validation), Ch. 21 (fetch + JSON), Ch. 22 (web APIs)
- Format: Rapid Q&A + one small live coding task (offer events/forms or fetch variant)

## Flow & Timing

- 0:00–0:15 Greeting and setup
  - Prompt: “Please share your screen in CodePen (HTML + JS panels ready).”
- 0:15–2:15 Concept Quickfire (6 short questions)
- 2:15–4:40 Live Coding Task (events/forms or fetch variant)
- 4:40–5:00 Wrap‑up (brief reflection + scoring notes)

## Concept Quickfire (aim ~10–15s each)

1) addEventListener basics
- Q: “What is the difference between addEventListener and setting onclick on an element?”
- Expected: addEventListener allows multiple handlers and better separation; inline/onclick is limited and mixes JS with markup.

2) preventDefault vs stopPropagation
- Q: “What’s the difference?”
- Expected: preventDefault cancels the default browser action; stopPropagation stops event bubbling.

3) Submit handling
- Q: “How do you prevent a form submit from reloading the page?”
- Expected: e.preventDefault() inside the submit handler.

4) Validation timing
- Q: “Which events are best for live validation vs end‑of‑field validation?”
- Expected: input for live; blur for after leaving the field.

5) fetch promises
- Q: “How do you access JSON from fetch?”
- Expected: fetch(url).then(res => res.json()).then(data => ...).

6) Response status
- Q: “How do you detect a 404/500 style failure?”
- Expected: check res.ok / res.status before parsing; throw to reach catch.

## Live Coding Task (pick A or B)

A) Events/forms variant (no network required)
- HTML to paste:

```html
<button id="btn">Click me</button>
<span id="count">0</span>
<form id="f">
  <input id="email" placeholder="email" />
  <button type="submit">Send</button>
</form>
```

- Prompt: “Increment the count each time the button is clicked. Add a submit handler that prevents default and logs 'OK' only if the email contains an '@'.”
- Acceptance:
  - addEventListener('click', ...) increments; addEventListener('submit', e.preventDefault()); basic '@' check and console.log.

B) Fetch variant (if network OK)
- HTML to paste:

```html
<button id="load">Load title</button>
<div id="out"></div>
```

- Prompt: “On click, fetch https://jsonplaceholder.typicode.com/todos/1 and display the 'title' in #out; handle errors in catch.”
- Acceptance:
  - fetch + res.json + set textContent; catch logs an error; no crash.

## Hints (offer only if stuck)

- Events: “Use textContent and Number(...) to increment from the DOM.”
- Fetch: “Check res.ok before res.json; set out.textContent to show results.”

## Sample Solutions (for instructor)

Events/forms
```js
const btn = document.getElementById('btn');
const count = document.getElementById('count');
btn.addEventListener('click', () => {
  count.textContent = String(Number(count.textContent) + 1);
});

document.getElementById('f').addEventListener('submit', (e) => {
  e.preventDefault();
  const v = document.getElementById('email').value;
  if (v.includes('@')) console.log('OK'); else console.log('Invalid');
});
```

Fetch
```js
const out = document.getElementById('out');
document.getElementById('load').addEventListener('click', () => {
  fetch('https://jsonplaceholder.typicode.com/todos/1')
    .then(res => { if (!res.ok) throw new Error(res.statusText); return res.json(); })
    .then(data => { out.textContent = data.title; })
    .catch(err => { out.textContent = 'Error: ' + err.message; });
});
```

## Scoring (25 pts)

- Concept Quickfire (10)
  - Correct, concise answers across 6 prompts (10)
- Coding (12)
  - Events/forms: correct handlers, preventDefault, and simple validation (12)
  - or Fetch: correct promise chain, render, and catch (12)
- Communication (3)
  - Thinks aloud, verifies with a quick run, responds to light guidance (3)

## Wrap‑Up Prompts (if time remains)

- “When would you use stopPropagation in the wild?”
- “One sentence on why you’d check res.ok before parsing.”

