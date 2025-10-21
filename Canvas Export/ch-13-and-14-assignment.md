# Ch. 13 & 14 Assignment: DOM Lab — Discover & Traverse

## Description

Combine Chapters 13 and 14 to practice core DOM skills: understand the DOM tree (element vs text nodes), navigate with `childNodes`/`parentNode`, select elements by tag/class/ID and with CSS selectors, read content and attributes, and work with classes. You’ll complete several small tasks using provided HTML snippets.

## Learning Objectives

- Access the DOM via `document` and identify node types.
- Navigate a page’s structure with `childNodes` and `parentNode`.
- Select elements with `getElementById`, `getElementsByTagName`, `getElementsByClassName`, `querySelector`, `querySelectorAll`.
- Inspect content via `innerHTML` and `textContent`; inspect attributes with `getAttribute`/`hasAttribute`.
- Use `classList` and `classList.contains()` to check classes.
- Handle NodeList vs Array and iterate selections safely.

## Setup (CodePen)

- Create a new CodePen named `Ch. 13 & 14 - DOM Lab`.
- Use both the HTML and JS panels.
- Open the Console (bottom bar → `Console`).
- For each task, paste the specific HTML snippet into the HTML panel (replace or comment/uncomment between tasks); put your JavaScript in the JS panel.

## Instructions

Work top‑to‑bottom. For each section:
- Paste the HTML snippet into the HTML panel.
- Add the requested JavaScript in the JS panel.
- Use `console.log()` for normal output and `console.error()` for error messages.

1) Show a node’s child (Ch. 13)
- HTML snippet:

```html
<h1>A title</h1>
<div>Some text with <a href="#">a link</a>.</div>
```

- JS requirements:
  - Write `showChild(node, index)` that logs the child at `index`.
  - If `node` is not an element node, log `"Wrong node type"` via `console.error()`.
  - If `index` is out of bounds, log `"Incorrect index"` via `console.error()`.

```js
// 1) Show a DOM object's child node
const showChild = (node, index) => {
  if (!node || node.nodeType !== document.ELEMENT_NODE) {
    console.error('Wrong node type');
    return;
  }
  const kids = node.childNodes; // NodeList (includes text nodes)
  if (index < 0 || index >= kids.length) {
    console.error('Incorrect index');
    return;
  }
  console.log(kids[index]);
};

// Tests
showChild(document.body, 1);  // Should show the h1 node (accounting for text nodes)
showChild(document.body, -1); // Incorrect index
showChild(document.body, 8);  // Incorrect index
showChild(document.body.childNodes[0], 0); // Wrong node type (likely a text node)
```

2) Selecting elements (Ch. 14)
- Replace the HTML panel with this snippet:

```html
<h1>Seven wonders of the world</h1>
<p>Do you know the seven wonders of the world?</p>
<div id="content">
  <h2>Wonders from Antiquity</h2>
  <p>This list comes to us from ancient times.</p>
  <ul class="wonders" id="ancient">
    <li class="exists">Great Pyramid of Giza</li>
    <li>Hanging Gardens of Babylon</li>
    <li>Lighthouse of Alexandria</li>
    <li>Statue of Zeus at Olympia</li>
    <li>Temple of Artemis at Ephesus</li>
    <li>Mausoleum at Halicarnassus</li>
    <li>Colossus of Rhodes</li>
  </ul>
  <h2>Modern wonders of the world</h2>
  <p>This list was decided by vote.</p>
  <ul class="wonders" id="new">
    <li class="exists">Petra</li>
    <li class="exists">Great Wall of China</li>
    <li class="exists">Christ the Redeemer</li>
    <li class="exists">Machu Picchu</li>
    <li class="exists">Chichen Itza</li>
    <li class="exists">Colosseum</li>
    <li class="exists">Taj Mahal</li>
  </ul>
  <h2>References</h2>
  <ul>
    <li><a href="https://en.wikipedia.org/wiki/Seven_Wonders_of_the_Ancient_World">Seven Wonders of the Ancient World</a></li>
    <li><a href="https://en.wikipedia.org/wiki/New7Wonders_of_the_World">New Wonders of the World</a></li>
  </ul>
  
</div>
```

- JS: Log the following counts using the indicated methods.

```js
// 2) Selection practice
console.log(document.getElementsByTagName('h2').length);      // Expect 3
console.log(document.querySelectorAll('#content p').length);   // Expect 2
console.log(document.querySelectorAll('.exists').length);      // Expect 8
console.log(document.querySelectorAll('#ancient > .exists').length); // Expect 1
```

3) Counting elements with CSS selectors (Ch. 14)
- Replace the HTML panel with this snippet:

```html
<h1>Mon rêve familier</h1>

<p>Je fais souvent ce rêve <span class="adjective">étrange</span> et <span class="adjective">pénétrant</span></p>
<p>D'une <span>femme <span class="adjective">inconnue</span></span>, et que j'aime, et qui m'aime</p>
<p>Et qui n'est, chaque fois, ni tout à fait la même</p>
<p>Ni tout à fait une autre, et m'aime et me comprend.</p>
```

- JS: Implement `countElements(selector)` that returns the number of matching elements, then log:

```js
// 3) countElements via querySelectorAll
const countElements = (selector) => document.querySelectorAll(selector).length;

console.log(countElements('p'));              // 4
console.log(countElements('.adjective'));     // 3
console.log(countElements('p .adjective'));   // 3
console.log(countElements('p > .adjective')); // 2
```

4) Handling attributes (Ch. 14)
- Replace the HTML panel with this snippet:

```html
<h1>Some musical instruments</h1>
<ul>
  <li id="clarinet" class="wind woodwind">
    The <a href="https://en.wikipedia.org/wiki/Clarinet">clarinet</a>
  </li>
  <li id="saxophone" class="wind woodwind">
    The <a href="https://en.wikipedia.org/wiki/Saxophone">saxophone</a>
  </li>
  <li id="trumpet" class="wind brass">
    The <a href="https://en.wikipedia.org/wiki/Trumpet">trumpet</a>
  </li>
  <li id="violin" class="chordophone">
    The <a href="https://en.wikipedia.org/wiki/Violin">violin</a>
  </li>
  <!-- After testing linkInfo(), add this and test again:
  <li id="harpsichord">
    The <a href="https://en.wikipedia.org/wiki/Harpsichord">harpsichord</a>
  </li>
  -->
  
</ul>
```

- JS: Implement `linkInfo()` to show total links and the targets of the first and last links. It must work when there are 0 links.

```js
// 4) linkInfo — total links, first and last href
function linkInfo() {
  const links = document.querySelectorAll('a');
  console.log('Total links:', links.length);
  if (links.length === 0) return;
  console.log('First link target:', links[0].getAttribute('href'));
  console.log('Last link target:', links[links.length - 1].getAttribute('href'));
}

linkInfo();
```

5) Handling classes (Ch. 14)
- Using the same instruments HTML, add `has(id, someClass)` that logs `true`/`false`, or logs an error via `console.error()` if the element is not found.

```js
// 5) has — test if element with id has a class
const has = (id, someClass) => {
  const el = document.getElementById(id);
  if (!el) {
    console.error('Element not found:', id);
    return;
  }
  console.log(el.classList.contains(someClass));
};

has('saxophone', 'woodwind');     // true
has('saxophone', 'brass');        // false
has('trumpet', 'brass');          // true
has('contrabass', 'chordophone'); // error
```

## Example Outputs

- Show child: incorrect index and wrong node type generate errors; valid index logs a Node.
- Wonders selection counts: `3`, `2`, `8`, `1`.
- Counting elements: `4`, `3`, `3`, `2`.
- linkInfo (before adding harpsichord): total `4`, prints first/last hrefs; after adding, total `5` with new last href.
- has: `true`, `false`, `true`, and an error for missing ID.

## What to Submit

- The URL to your public CodePen `Ch. 13 & 14 - DOM Lab`.
- A note that tasks 1–5 run and produce the expected results (update the HTML per section).

## Grading (10 pts)

- `showChild(node, index)` with proper error handling (2)
- Correct use of selection methods for counts (2)
- `countElements(selector)` works for given queries (2)
- `linkInfo()` handles 0/≥1 links, shows first/last (2)
- `has(id, class)` logs true/false and errors appropriately (2)

## Tips & Troubleshooting

- NodeList is not a real Array; use `Array.from()` if you need array methods.
- `innerHTML` includes markup; `textContent` is text only.
- `getAttribute()` vs property access (e.g., `href`) can show different forms (absolute vs as‑written).
- Whitespace between tags creates text nodes — indexes in `childNodes` include them.
