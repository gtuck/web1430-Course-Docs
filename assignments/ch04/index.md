# Ch. 4 Assignment: Loops Lab — Repeat Statements

## Description

Practice Chapter 4 looping by writing programs with `while` and `for`, controlling counters, avoiding infinite loops, checking number parity with `%`, validating user input with loops, generating multiplication tables, and implementing the classic FizzBuzz. You’ll build small, focused tasks in a single CodePen.

## Learning Objectives

- Use `while` and `for` loops to repeat code.
- Initialize, test, and update loop counters safely.
- Avoid infinite loops by ensuring conditions eventually become false.
- Use the modulo operator `%` to detect even and odd numbers.
- Validate user input with loops; convert input with `Number()`.
- Generate structured output (e.g., multiplication tables) via loops.

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 4 - Loops Lab`.
- Use the JS panel only (no HTML/CSS).
- Open the CodePen Console (click `Console` at the bottom).
- Optional: Pen Settings → Behavior → enable “Clear Console on Run”.

## Instructions

Work top‑to‑bottom in the JS panel. Add comments to separate each task. For tasks 1–3, try both a `while` and a `for` version where indicated.

1) Carousel — 10 turns
- Show the turn number from 1 to 10.

```js
// 1) Carousel — 10 turns (while)
let turn = 1;
while (turn <= 10) {
  console.log('Turn ' + turn);
  turn++;
}

// 1) Carousel — 10 turns (for)
for (let i = 1; i <= 10; i++) {
  console.log('Turn ' + i);
}
```

2) Carousel — user‑defined turns
- Ask how many turns to run, then show each turn number.

```js
// 2) Carousel — user-defined turns
const totalTurns = Number(prompt('How many turns?'));
if (!Number.isNaN(totalTurns) && totalTurns > 0) {
  for (let i = 1; i <= totalTurns; i++) {
    console.log('Turn ' + i);
  }
} else {
  console.log('Invalid number of turns');
}
```

3) Parity — even and odd
- First, show even numbers between 1 and 10.
- Then, also show odd numbers.
- Finally, ask for a starting number and show exactly 10 numbers (starting number included), each labeled even or odd.

```js
// 3a) Even numbers 1..10 (for)
for (let i = 1; i <= 10; i++) {
  if (i % 2 === 0) {
    console.log(i + ' is even');
  }
}

// 3b) Even and odd 1..10 (while)
let n = 1;
while (n <= 10) {
  if (n % 2 === 0) {
    console.log(n + ' is even');
  } else {
    console.log(n + ' is odd');
  }
  n++;
}

// 3c) Exactly 10 numbers starting from user input
const start = Number(prompt('Enter a starting number:'));
if (!Number.isNaN(start)) {
  for (let k = 0; k < 10; k++) {
    const value = start + k;
    if (value % 2 === 0) {
      console.log(value + ' is even');
    } else {
      console.log(value + ' is odd');
    }
  }
} else {
  console.log('Invalid starting number');
}
```

4) Input validation
- Keep asking for a number until it is `<= 100`.
- Then improve: keep asking until it is between `50` and `100` (inclusive).

```js
// 4a) Ask until <= 100
let value = Number(prompt('Enter a number (<= 100):'));
while (Number.isNaN(value) || value > 100) {
  value = Number(prompt('Enter a number (<= 100):'));
}
console.log('Accepted:', value);

// 4b) Ask until between 50 and 100 inclusive
let bounded = Number(prompt('Enter a number between 50 and 100:'));
while (Number.isNaN(bounded) || bounded < 50 || bounded > 100) {
  bounded = Number(prompt('Enter a number between 50 and 100:'));
}
console.log('Accepted (50..100):', bounded);
```

5) Multiplication table (with validation)
- Ask for a number between 2 and 9; reprompt until valid.
- Show its multiplication table from 1 to 10.

```js
// 5) Multiplication table 2..9
let m = Number(prompt('Enter a number (2..9):'));
while (Number.isNaN(m) || m < 2 || m > 9) {
  m = Number(prompt('Enter a number (2..9):'));
}
for (let i = 1; i <= 10; i++) {
  console.log(m + ' x ' + i + ' = ' + (m * i));
}
```

6) Neither yes nor no
- Keep asking the user for text until they type `yes` or `no`. Then log a closing message.

```js
// 6) Neither yes nor no
let text = '';
while (text !== 'yes' && text !== 'no') {
  text = prompt('Type "yes" or "no" to end:');
}
console.log('Game over.');
```

7) FizzBuzz
- Show numbers from 1 to 100. Replace:
  - Multiples of 3 with `Fizz`
  - Multiples of 5 (but not 3) with `Buzz`
  - Multiples of both 3 and 5 with `FizzBuzz`

```js
// 7) FizzBuzz
for (let i = 1; i <= 100; i++) {
  if (i % 15 === 0) {
    console.log('FizzBuzz');
  } else if (i % 3 === 0) {
    console.log('Fizz');
  } else if (i % 5 === 0) {
    console.log('Buzz');
  } else {
    console.log(i);
  }
}
```

## Example Outputs

- Carousel (10 turns) begins with: `Turn 1`, `Turn 2`, `Turn 3` … and ends at `Turn 10`.
- Parity from 5 (10 numbers): `5 is odd`, `6 is even`, …, `14 is even`.
- Multiplication table for 7 includes: `7 x 1 = 7`, `7 x 10 = 70`.
- FizzBuzz includes: `1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz, ...`.

## What to Submit

- The URL to your public CodePen `Ch. 4 - Loops Lab`.
- A short note that tasks 1–7 run and produce the expected messages.

## Grading (25 pts)

- Carousel 10‑turn and user‑defined versions (5)
- Parity: even/odd and exactly 10 numbers from start (5)
- Input validation loops (`<=100` and `50..100`) (5)
- Multiplication table 2..9 with validation (5)
- Neither yes nor no (3)
- FizzBuzz with correct precedence/order (2)

## Tips & Troubleshooting

- Infinite loops: ensure counters update and conditions will become false.
- Conversions: wrap `prompt()` results with `Number()` for numeric checks.
- Validation: prefer `while (invalid) { reprompt }` patterns.
- For‑loop counters: avoid modifying the counter inside the loop body.
