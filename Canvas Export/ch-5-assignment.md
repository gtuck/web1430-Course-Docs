# Ch. 5 Assignment: Functions Lab — Define and Use Functions

## Description

Practice Chapter 5 function basics: declare functions, pass parameters, return values, and reuse them. You’ll implement small, focused utilities (square, min, circle math, greet) and test each with sample calls, including simple user input and number conversion.

## Learning Objectives

- Declare functions with the `function` keyword.
- Use parameters and return values to produce results.
- Reuse functions by calling them with different arguments.
- Use `const` for constants (e.g., `pi`) and avoid unnecessary global side effects.
- Read input with `prompt()` and convert with `Number()` when needed.
- Display results with `console.log()` clearly.

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 5 - Functions Lab`.
- Use the JS panel only (no HTML/CSS).
- Open the CodePen Console (click `Console` at the bottom).
- Optional: Pen Settings → Behavior → enable “Clear Console on Run”.

## Instructions

Work top‑to‑bottom in the JS panel. Add comments to separate tasks. For each function, add a few test calls and log the results.

1) square(n)
- Write a function that returns the square of a number.

```js
// 1) square(n)
function square(n) {
  return n * n;
}

console.log('square(0) =', square(0));
console.log('square(2) =', square(2));
console.log('square(5) =', square(5));
```

2) min(a, b)
- Write a function that returns the smaller of two numbers. If they’re equal, return either.

```js
// 2) min(a, b)
function min(a, b) {
  if (a < b) {
    return a;
  } else if (b < a) {
    return b;
  } else {
    return a; // equal case
  }
}

console.log('min(2, 5) =', min(2, 5));
console.log('min(10, 3) =', min(10, 3));
console.log('min(7, 7) =', min(7, 7));
```

3) Circle math — circumference(r) and area(r)
- Use a constant `pi = 3.14`.
- Write `circumference(r)` that returns `2 * pi * r`.
- Write `area(r)` that returns `pi * r * r`.
- Ask the user for a radius; convert to number; log both results.

```js
// 3) Circle math
const pi = 3.14;

function circumference(r) {
  return 2 * pi * r;
}

function area(r) {
  return pi * r * r;
}

const radiusInput = prompt('Enter a radius:');
const radius = Number(radiusInput);
if (!Number.isNaN(radius) && radius >= 0) {
  console.log('circumference(' + radius + ') =', circumference(radius));
  console.log('area(' + radius + ') =', area(radius));
} else {
  console.log('Invalid radius');
}
```

4) greet(firstName, lastName)
- Write a function that returns a greeting string like `Hello, Ada Lovelace!`.
- Ask the user for first and last names and show the greeting.

```js
// 4) greet(firstName, lastName)
function greet(firstName, lastName) {
  return 'Hello, ' + firstName + ' ' + lastName + '!';
}

const first = prompt('Enter your first name:');
const last = prompt('Enter your last name:');
console.log(greet(first, last));
```

5) Fix‑me mini‑exercises
- Correct each snippet so it works as intended.

```js
// 5a) Missing return — should print 9
// function triple(x) { x * 3; }
function triple(x) { return x * 3; }
console.log(triple(3));

// 5b) Parameter order — should print 2 then 5
// function first(a, b) { return b; }
function first(a, b) { return a; }
console.log(first(2, 5));

// 5c) Name mismatch — should call the declared function
// function sq(n) { return n * n; }
// console.log(square(4));
function sq(n) { return n * n; }
console.log(sq(4));
```

## Example Output

Your output will vary based on inputs. Sample checkpoints:

```
square(0) = 0
square(2) = 4
square(5) = 25
min(2, 5) = 2
min(10, 3) = 3
min(7, 7) = 7
circumference(3) = 18.84
area(3) = 28.26
Hello, Ada Lovelace!
9
2
16
```

## What to Submit

- The URL to your public CodePen `Ch. 5 - Functions Lab`.
- A short note that tasks 1–5 run and produce the expected messages.

## Grading (10 pts)

- `square(n)` implemented with correct tests (2)
- `min(a, b)` implemented with equal case handled (2)
- Circle math: `const pi`, `circumference(r)`, `area(r)`, input conversion (3)
- `greet(firstName, lastName)` and sample inputs (1)
- Fix‑me mini‑exercises corrected (2)

## Tips & Troubleshooting

- Always `return` a value from functions that compute a result.
- Keep constants like `pi` in `const` and reuse them.
- Convert prompt input with `Number()` before numeric math.
- Name functions clearly; make test calls after each definition.

