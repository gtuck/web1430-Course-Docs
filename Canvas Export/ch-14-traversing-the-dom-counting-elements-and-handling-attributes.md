# Assignment: Ch. 14 - Traversing the DOM - Counting elements & Handling attributes

## Description

In this assignment, you will practice traversing the DOM by counting elements and handling attributes using JavaScript. Follow the steps below to complete the assignment:

## Objective
## Instructions

1. Create a new pen on [codepen.io](https://codepen.io/) and name it "Traversing the DOM".
2. Copy the provided HTML and JavaScript samples into your pen.
3. Complete the three JavaScript functions as described below.

**HTML:**

```
<h1>Adventures in HTML and JavaScript!</h1>

<h2>Mon rêve familier</h2>
<p>Je fais rêve <span class="adjective">étrange</span> et <span class="adjective">pénétrant</span></p>
<p>D'une <span>femme <span class="adjective">inconnue</span></span>, et que j'aime, et qui m'aime</p>
<p>Et qui n'est, chaque fois, ni tout à fait la même</p>
<p>Ni tout à fait une autre, et m'aime et me comprend.</p>

<h2>Some musical instruments</h2>
<ul>
    <li id="clarinet" class="wind woodwind">The <a href="https://en.wikipedia.org/wiki/Clarinet">clarinet</a></li>
    <li id="saxophone" class="wind woodwind">The <a href="https://en.wikipedia.org/wiki/Saxophone">saxophone</a></li>
    <li id="trumpet" class="wind brass">The <a href="https://en.wikipedia.org/wiki/Trumpet">trumpet</a></li>
    <li id="violin" class="chordophone">The <a href="https://en.wikipedia.org/wiki/Violin">violin</a></li>
    <li id="harpsichord">The <a href="https://en.wikipedia.org/wiki/Harpsichord">harpsichord</a></li>
</ul>
```

**JavaScript:**

1. Write a `countElements()` function in the 'arrow function' style. This function should take a CSS selector as a parameter and return the number of corresponding elements. It should be written in one line of code.
Sample function calls and outputs for `countElements()` function:

  - `console.log(countElements("p")); // Expected output: 4`
  - `console.log(countElements(".adjective")); // Expected output: 3`
  - `console.log(countElements("p .adjective")); // Expected output: 3`
  - `console.log(countElements("p > .adjective")); // Expected output: 2`

2. Write a `linkInfo()` function in the 'function declaration' style. This function should display the total number of links, the target (href) of the first link, and the target (href) of the last link.
Sample function call and output for `linkInfo()` function:

  - `linkInfo();`
  - `// Expected output: `
  - `5`
  - `https://en.wikipedia.org/wiki/Clarinet`
  - `https://en.wikipedia.org/wiki/Harpsichord`

3. Write a `has(id, someClass)` function in the 'function expression' style. This function should test if an element designated by its ID has a certain class. It should return `true`, `false`, or `undefined` if the element can't be found.
Sample function calls and outputs for `has(id, someClass)` function:

  - `console.log(has("saxophone", "woodwind")); // Expected output: true`
  - `console.log(has("saxophone", "brass")); // Expected output: false`
  - `console.log(has("trumpet", "brass")); // Expected output: true`
  - `console.log(has("contrabass", "chordophone")); // Expected output: undefined`

Once you have completed the assignment, save your pen and submit the URL of your saved pen as your assignment submission.

## What to Submit

Submit the URL to your CodePen.