# Interview 02 Script — Chapters 7–15 (5 minutes)

- Duration: 5 minutes on Zoom (screen-share required)
- Scope: Ch. 7 (arrays), Ch. 8 (strings), Ch. 9 (classes/OOP), Ch. 10 (map/filter/reduce), Ch. 13–15 (DOM selection + updates)
- Format: Rapid Q&A + a small coding task solved live (offer DOM or array/FP variant)

## Flow & Timing

- 0:00–0:15 Greeting and setup
  - Prompt: “Please share your screen in CodePen (HTML + JS panels ready).”
- 0:15–2:15 Concept Quickfire (6 short questions)
- 2:15–4:40 Live Coding Task (DOM or FP variant)
- 4:40–5:00 Wrap‑up (brief reflection + scoring notes)

## Concept Quickfire (aim ~10–15s each)

1) Arrays
- Q: “When would you use for...of vs forEach on an array?”
- Expected: for...of for simple value iteration; forEach takes a callback, returns undefined.

2) Strings
- Q: “Are strings mutable in JS? Show a quick way to uppercase 'js'.”
- Expected: immutable; 'js'.toUpperCase().

3) OOP `this`
- Q: “Inside an object method, what does `this` usually refer to?”
- Expected: the object the method was called on.

4) map vs filter vs reduce
- Q: “One sentence each: map, filter, reduce.”
- Expected: map transforms; filter selects; reduce aggregates to one value.

5) DOM selection
- Q: “When prefer querySelector over getElementById?”
- Expected: complex CSS selectors or when not selecting strictly by id.

6) Content vs HTML
- Q: “Difference between textContent and innerHTML?”
- Expected: textContent is plain text; innerHTML parses/sets markup.

## Live Coding Task (pick A or B)

A) DOM variant (if CodePen HTML panel is ready)
- HTML to paste:

```html
<ul id="items"></ul>
```

- Prompt: “Given const data = ['Tea','Coffee','Juice'], build li elements using createElement and appendChild (no innerHTML). Then add a class 'drink' to each li.”
- Acceptance:
  - Loops over array, createElement('li'), textContent, append, classList.add('drink').

B) Array/FP variant (no DOM)
- Prompt: “Given const products = [{name:'Pen',price:2,inStock:true},{name:'Book',price:10,inStock:false},{name:'Tea',price:5,inStock:true}], return an array of names of in‑stock items priced >= 3, uppercased.”
- Acceptance: products.filter(...).map(...). Possibly chain; no mutation.

## Hints (offer only if stuck)

- DOM: “Use document.getElementById('items') and li.textContent = value.”
- FP: “Filter by inStock and price, then map to name.toUpperCase().”

## Sample Solutions (for instructor)

DOM variant
```js
const data = ['Tea', 'Coffee', 'Juice'];
const list = document.getElementById('items');
data.forEach(x => {
  const li = document.createElement('li');
  li.textContent = x;
  li.classList.add('drink');
  list.appendChild(li);
});
```

FP variant
```js
const products = [
  {name:'Pen', price:2, inStock:true},
  {name:'Book', price:10, inStock:false},
  {name:'Tea', price:5, inStock:true}
];
const names = products
  .filter(p => p.inStock && p.price >= 3)
  .map(p => p.name.toUpperCase());
console.log(names);
```

## Scoring (25 pts)

- Concept Quickfire (10)
  - Correct, concise answers across 6 prompts (10)
- Coding (12)
  - DOM variant: correct selection/creation/appending and class usage (12)
  - or FP variant: correct filter + map chaining and no mutation (12)
- Communication (3)
  - Thinks aloud, verifies with a quick run, responds to light guidance (3)

## Wrap‑Up Prompts (if time remains)

- “When would you prefer reduce over a loop?”
- “One sentence on when to avoid innerHTML in favor of createElement.”

