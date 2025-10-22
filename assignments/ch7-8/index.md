# Ch. 7 & 8: Arrays and Strings Lab

## Description

Practice Chapters 7 and 8 together: store and process data in arrays, iterate with different loop styles, update arrays, and manipulate strings (length, case, indexing, iteration, search). Build small tasks in one CodePen to solidify fundamentals.

## Learning Objectives

- Create and update arrays; use `.length`, indexing, and iteration (`for`, `forEach`, `for...of`).
- Add and remove elements with `push`, `unshift`, `pop`, and `splice`.
- Compute aggregates (sum, max) by iterating arrays.
- Read multiple inputs with `prompt()` and store them in arrays.
- Use string length, case conversion (`toLowerCase`, `toUpperCase`), indexing, and iteration.
- Build and search strings with simple logic and methods like `indexOf`, `startsWith`, `endsWith`, and `split` (where useful).

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 7 & 8 - Arrays and Strings Lab`.
- Use the JS panel only (no HTML/CSS).
- Open the CodePen Console (click `Console` at the bottom).
- Optional: Pen Settings → Behavior → enable “Clear Console on Run”.

## Instructions

Work top‑to‑bottom in the JS panel. Add comments to separate tasks.

1) Musketeers
- Create an array `musketeers` with `"Athos"`, `"Porthos"`, `"Aramis"`.
- Show each element using a `for` loop.
- Add `"D'Artagnan"` with `push`, then show each element using `forEach`.
- Remove `"Aramis"` and then show each element using `for...of`.

```js
// 1) Musketeers
let musketeers = ['Athos', 'Porthos', 'Aramis'];

// a) for loop
for (let i = 0; i < musketeers.length; i++) {
  console.log(musketeers[i]);
}

// b) add D'Artagnan, then forEach
musketeers.push("D'Artagnan");
musketeers.forEach(name => {
  console.log(name);
});

// c) remove Aramis (generic)
const aramisIndex = musketeers.indexOf('Aramis');
if (aramisIndex !== -1) {
  musketeers.splice(aramisIndex, 1);
}

// d) for...of
for (const name of musketeers) {
  console.log(name);
}
```

2) Sum of values
- Create `values = [3, 11, 7, 2, 9, 10]`. Compute and log the sum (should reflect changes if the array changes).

```js
// 2) Sum of values
const values = [3, 11, 7, 2, 9, 10];
let sum = 0;
for (const n of values) {
  sum += n;
}
console.log('sum =', sum); // 42
```

3) Array maximum
- Using the same `values` array (or another), compute and log the maximum value generically.

```js
// 3) Array maximum
let max = values[0];
for (const n of values) {
  if (n > max) {
    max = n;
  }
}
console.log('max =', max); // 11
```

4) List of words (until "stop")
- Ask the user for words until they type exactly `stop`.
- Then show each of the entered words, excluding `stop`.

```js
// 4) List of words
const words = [];
while (true) {
  const w = prompt('Enter a word (type "stop" to finish):');
  if (w === null) break; // user canceled
  if (w === 'stop') break;
  words.push(w);
}
// show words
for (const w of words) {
  console.log(w);
}
```

5) Word info
- Ask for a single word; show its length, lowercase, and uppercase values.

```js
// 5) Word info
const word = prompt('Enter a word:') || '';
console.log('length:', word.length);
console.log('lowercase:', word.toLowerCase());
console.log('uppercase:', word.toUpperCase());
```

6) Vowel count (a, e, i, o, u)
- Count the number of vowels in the entered word (treat input case‑insensitively).

```js
// 6) Vowel count
const lower = word.toLowerCase();
let vowels = 0;
for (const ch of lower) {
  if (ch === 'a' || ch === 'e' || ch === 'i' || ch === 'o' || ch === 'u') {
    vowels++;
  }
}
console.log('vowels:', vowels);
```

7) Backwards word
- Show the word written backwards.

```js
// 7) Backwards word
let reversed = '';
for (let i = word.length - 1; i >= 0; i--) {
  reversed += word[i];
}
console.log('reversed:', reversed);
```

8) Palindrome (ignore punctuation, spacing, and case)
- Normalize the input by keeping only letters and digits, converting to lowercase.
- Check if the normalized string reads the same forward and backward.

```js
// 8) Palindrome check
function isAlphaNum(ch) {
  const c = ch.toLowerCase();
  const isLetter = c >= 'a' && c <= 'z';
  const isDigit = c >= '0' && c <= '9';
  return isLetter || isDigit;
}

let cleaned = '';
for (const ch of (prompt('Enter a word or phrase to test palindrome:') || '')) {
  if (isAlphaNum(ch)) {
    cleaned += ch.toLowerCase();
  }
}

let cleanedReversed = '';
for (let i = cleaned.length - 1; i >= 0; i--) {
  cleanedReversed += cleaned[i];
}

const isPal = cleaned.length > 0 && cleaned === cleanedReversed;
console.log('palindrome:', isPal);
```

## Example Outputs

- Musketeers after removal might show: `Athos`, `Porthos`, `D'Artagnan`.
- Sum: `sum = 42`; Max: `max = 11` for `[3, 11, 7, 2, 9, 10]`.
- Words list (input: apple, banana, stop): outputs `apple`, `banana`.
- Word info for `JavaScript`: `length: 10`, `lowercase: javascript`, `uppercase: JAVASCRIPT`.
- Vowel count for `JavaScript`: `vowels: 3`.
- Backwards for `radar`: `reversed: radar`.
- Palindrome: `radar` → `palindrome: true`; `A man, a plan, a canal: Panama!` → `palindrome: true`.

## What to Submit

- The URL to your public CodePen `Ch. 7 & 8 - Arrays and Strings Lab`.
- A short note that tasks 1–8 run and produce the expected messages.

## Grading (25 pts)

- Musketeers: correct iterations and dynamic add/remove (8)
- Sum and maximum computed generically from the array (5)
- List‑of‑words loop and display excluding `stop` (2)
- Word info: length and case conversions (3)
- Vowel count (case‑insensitive) (3)
- Reverse and palindrome ignoring spaces/punctuation/case (4)

## Tips & Troubleshooting

- Loops: be careful with start/end indexes and off‑by‑one errors.
- Iteration: prefer `for...of` when you don’t need indexes; use classic `for` for index access.
- Array updates: `push` adds to end; `unshift` adds to start; `pop` removes last; `splice(i, n)` removes `n` elements from index `i`.
- Strings are immutable; build new strings when reversing or filtering.
- Palindrome normalization: keep letters/digits and lower‑case them before comparing.
