# Ch. 2 Assignment: Console Practice — Variables, Swap, Increment

## Description

Practice core Chapter 2 skills: declaring variables with `let` and `const`, assigning values, incrementing numbers, evaluating expressions, converting user input with `Number()`, and swapping variable values. You’ll implement and verify several swap techniques and explore common pitfalls.

## Learning Objectives

- Declare variables with `let` and constants with `const`.
- Assign and reassign values using `=` and update with `+=` / `++`.
- Predict and verify results of basic expressions and operator precedence.
- Swap two variable values using different approaches (with and without a temp variable).
- Use `prompt()` and `Number()` to read and convert user input.
- Display information with `console.log()` (including multiple comma‑separated values).

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 2 - Console Practice`.
- Use the JS panel only (no HTML/CSS required).
- Open the CodePen Console (click `Console` at the bottom) to view output.
- Optional: Pen Settings → Behavior → enable “Clear Console on Run”.

## Instructions

Work top‑to‑bottom in the JS panel. Comment your sections. Unless noted, use `let` for variables that change and `const` for values that won’t change.

1) Starter and observation
- Copy this program and run it. Observe the initial values.

```js
// 1) Starter and observation
let number1 = 5;
let number2 = 3;

// TODO: enter your swap code below this line (and nowhere else!)

console.log(number1); // Should show 3 after swap
console.log(number2); // Should show 5 after swap
```

2) Swap using a temporary variable (classic)
- Insert these three lines where the TODO says. Then run and verify the logs show 3 then 5.

```js
// 2) Temp variable swap
let temp = number1; // store the first value
number1 = number2;  // move second into first
number2 = temp;     // put original first into second
```

3) Reset and try arithmetic swap (no temp)
- Above the swap, reset `number1` and `number2` to new values (e.g., 8 and 4). Then insert the lines below at the TODO.
- This method works for numbers but not for strings.

```js
// 3) Arithmetic swap
number1 = number1 + number2;
number2 = number1 - number2;
number1 = number1 - number2;
```

4) Increment practice
- Create a counter and update it with `+=` and `++`.

```js
// 4) Increment practice
let counter = 0;      // counter contains 0
counter += 1;         // counter contains 1
counter++;            // counter contains 2
console.log('counter:', counter); // Expect 2
```

5) User input + swap (with Number())
- Ask the user for two numbers, convert them, then swap with a temp variable. Log before and after.

```js
// 5) Prompt + Number conversion + swap
const inputA = prompt('Enter the first number:');
const inputB = prompt('Enter the second number:');
let a = Number(inputA);
let b = Number(inputB);

console.log('Before swap:', a, b);

// swap with a temp variable
let t = a;
a = b;
b = t;

console.log('After swap:', a, b);
```

6) Expressions and precedence (mini‑prediction)
- Predict each result in a comment, then log to check.

```js
// 6) Expressions and precedence
// Predict results, then verify:
// a) 3 + 2 * 4 = ? (expect 11)
// b) (3 + 2) * 4 = ? (expect 20)
console.log(3 + 2 * 4);
console.log((3 + 2) * 4);
```

7) Optional: constants and reassignment error (read only)
- The line changing `pi` is commented out because it would cause an error. Read and understand why.

```js
// 7) Constants example (do not uncomment the reassignment)
const pi = 3.14;     // a constant
// pi = 3.14159;     // Error if uncommented: Assignment to constant variable.
console.log('pi is', pi);
```

## Example Output

Your output will vary, but key checkpoints should resemble:

```
3
5
counter: 2
Before swap: 12 7
After swap: 7 12
11
20
pi is 3.14
```

## What to Submit

- The URL to your public CodePen `Ch. 2 - Console Practice`.
- Note in the Pen description that all steps (1–7) are implemented and the console shows the expected checkpoints.

## Grading (10 pts)

- Temp variable swap works and prints 3 then 5 (3)
- Arithmetic swap works after reset (2)
- Correct use of `let`/`const`, assignment, and comments (2)
- Increment demo shows expected value (1)
- Prompt + `Number()` conversion + swap logs before/after (2)

## Tips & Troubleshooting

- If prompt input is missing or non‑numeric, `Number()` yields `NaN`. Try again with numeric input.
- If your arithmetic swap fails, ensure you reset `number1`/`number2` before swapping and use numbers.
- Use `console.log(n1, n2)` with comma separation to print multiple values in one call.
