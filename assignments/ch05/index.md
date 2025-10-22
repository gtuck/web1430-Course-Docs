# Ch. 5: Write Functions — Declarations, Arrow, Reuse

## Description

Practice Chapter 5 function basics: declare functions, pass parameters, return values, and reuse them. Build the exact chapter exercises: Improved hello, number squaring (with a loop), minimum of two numbers, a basic calculator, and circle circumference/area using `Math.PI` and exponentiation.

## Learning Objectives

- Declare functions with the `function` keyword and with arrow syntax.
- Use parameters and `return` values correctly; call functions to reuse logic.
- Convert user input with `Number()` where numeric math is required.
- Use `Math.PI` and the exponentiation operator `**` for circle math.
- Apply control flow inside functions (e.g., `if/else`, `switch`).
- Log results clearly with `console.log()`.

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 5 - Functions Lab`.
- Use the JS panel only (no HTML/CSS).
- Open the CodePen Console (click `Console` at the bottom).
- Optional: Pen Settings → Behavior → enable “Clear Console on Run”.

## Instructions

Work top‑to‑bottom in the JS panel. Add comments to separate tasks. Follow the chapter tasks closely.

1) Improved hello
- Complete the program so it asks the user for first and last names, then shows the result of `sayHello()`.

```js
// 1) Improved hello — complete the program
function sayHello(firstName, lastName) {
  const message = `Hello, ${firstName} ${lastName}!`;
  return message;
}

// TODO: ask user for first and last name
const first = prompt('Enter your first name:');
const last = prompt('Enter your last name:');

// TODO: call sayHello() and show its result
console.log(sayHello(first, last));
```

2) Number squaring — two functions, then a loop
- Make both functions work, then show squares for numbers 0..10 using a loop (don’t write 11 manual calls!).

```js
// 2) Number squaring
// Square the given number x
function square1(x) {
  return x * x;
}

// Square the given number x (arrow syntax)
const square2 = x => x * x;

console.log(square1(0)); // 0
console.log(square1(2)); // 4
console.log(square1(5)); // 25

console.log(square2(0)); // 0
console.log(square2(2)); // 4
console.log(square2(5)); // 25

// Now show squares for 0..10 using a loop
for (let i = 0; i <= 10; i++) {
  console.log(i + ' squared = ' + square1(i));
}
```

3) Minimum of two numbers
- Implement `min(a, b)` (ignore `Math.min`).

```js
// 3) Minimum of two numbers
function min(a, b) {
  if (a < b) return a;
  if (b < a) return b;
  return a; // equal case
}

console.log(min(4.5, 5)); // 4.5
console.log(min(19, 9));  // 9
console.log(min(1, 1));   // 1
```

4) Calculator
- Complete `calculate(a, op, b)` to support `+`, `-`, `*`, and `/`.

```js
// 4) Calculator
function calculate(a, op, b) {
  if (op === '+') return a + b;
  if (op === '-') return a - b;
  if (op === '*') return a * b;
  if (op === '/') return a / b; // JS returns Infinity for divide by 0
  return NaN; // unsupported operator
}

console.log(calculate(4, '+', 6));  // 10
console.log(calculate(4, '-', 6));  // -2
console.log(calculate(2, '*', 0));  // 0
console.log(calculate(12, '/', 0)); // Infinity
```

5) Circumference and area of a circle
- Write `circumference(r)` and `area(r)` using `Math.PI` and `**`. Ask the user for a radius, convert it, and log both results.

```js
// 5) Circle math with Math.PI and **
function circumference(r) {
  return 2 * Math.PI * r;
}

function area(r) {
  return Math.PI * (r ** 2);
}

const radiusInput = prompt('Enter a radius:');
const radius = Number(radiusInput);
if (!Number.isNaN(radius) && radius >= 0) {
  console.log('circumference(' + radius + ') = ' + circumference(radius));
  console.log('area(' + radius + ') = ' + area(radius));
} else {
  console.log('Invalid radius');
}
```

## Example Outputs

Your output will vary based on inputs. Sample checkpoints:

```
Hello, Ada Lovelace!
0
4
25
0
4
25
0 squared = 0
...
10 squared = 100
4.5
9
1
10
-2
0
Infinity
circumference(3) = 18.84955592153876
area(3) = 28.274333882308138
```

## What to Submit

- The URL to your public CodePen `Ch. 5 - Functions Lab`.
- A short note that tasks 1–5 run and produce the expected messages.

## Grading (25 pts)

- Improved hello: prompts and shows `sayHello()` result (3)
- Number squaring: `square1` and arrow `square2` plus loop 0..10 (7)
- `min(a, b)` implemented and tested (5)
- `calculate(a, op, b)` handles +, -, *, / (incl. divide by 0) (5)
- Circle math: `circumference(r)` and `area(r)` using `Math.PI` and `**` with input conversion (5)

## Tips & Troubleshooting

- Always `return` from functions that compute a result.
- Arrow functions are concise; use them when appropriate.
- Convert prompt input with `Number()` before numeric math.
- Prefer strict equality `===` when comparing operators/strings.
- Use `Math.PI` for π and `**` for powers.
