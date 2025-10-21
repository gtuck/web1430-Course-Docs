# Ch. 3 Assignment: Console Practice — Conditions and Switch

## Description

Practice Chapter 3 branching: write conditionals with `if`, `else if`, and `else`; compare values with `===`, `!==`, `<`, `<=`, `>`, `>=`; combine conditions using `&&`, `||`, `!`; and select among multiple choices with `switch`. You’ll build several small console programs in one CodePen.

## Learning Objectives

- Use `if`, `else if`, `else` to branch program flow.
- Compare values with strict operators (`===`, `!==`) and numeric comparisons.
- Combine boolean expressions with `&&`, `||`, and negate with `!`.
- Implement multi-way branching with `switch` and `default`, using `break` correctly.
- Read user input with `prompt()` and convert to numbers with `Number()` when needed.
- Log results clearly with `console.log()`.

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 3 - Conditions and Switch`.
- Use the JS panel only (no HTML/CSS).
- Open the CodePen Console (click `Console` in the bottom bar).
- Optional: Pen Settings → Behavior → enable “Clear Console on Run”.

## Instructions

Work top‑to‑bottom in the JS panel. Add comments to mark each task.

1) Classify a number (if / else if / else)
- Ask for a number, then log whether it’s positive, negative, or zero.

```js
// 1) Classify a number
const n = Number(prompt('Enter a number:'));
if (n > 0) {
  console.log('The number is positive');
} else if (n < 0) {
  console.log('The number is negative');
} else {
  console.log('The number is zero');
}
```

2) Range check with && and ||
- Ask for a number and log whether it’s between 0 and 100 (inclusive). Otherwise, report it’s outside the range.

```js
// 2) Range check
const r = Number(prompt('Enter a number between 0 and 100:'));
if ((r >= 0) && (r <= 100)) {
  console.log(r + ' is between 0 and 100');
} else {
  console.log(r + ' is outside 0–100');
}
```

3) Following day (switch)
- Ask for a day of the week: `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`, `Sunday`.
- Use `switch` to log "Tomorrow is <NextDay>".
- For invalid input, log "Unrecognized day name".
- Note: require exact capitalization as shown.

```js
// 3) Following day (switch)
const day = prompt('Enter a day of the week (e.g., Monday):');
switch (day) {
  case 'Monday':
    console.log('Tomorrow is Tuesday');
    break;
  case 'Tuesday':
    console.log('Tomorrow is Wednesday');
    break;
  case 'Wednesday':
    console.log('Tomorrow is Thursday');
    break;
  case 'Thursday':
    console.log('Tomorrow is Friday');
    break;
  case 'Friday':
    console.log('Tomorrow is Saturday');
    break;
  case 'Saturday':
    console.log('Tomorrow is Sunday');
    break;
  case 'Sunday':
    console.log('Tomorrow is Monday');
    break;
  default:
    console.log('Unrecognized day name');
}
```

4) Multiple choices (weather)
- Ask for the weather: `sunny`, `windy`, `rainy`, or `snowy`. Use `if / else if / else` to log an appropriate message.

```js
// 4) Multiple choices (weather)
const weather = prompt("What's the weather like?");
if (weather === 'sunny') {
  console.log('T-shirt time!');
} else if (weather === 'windy') {
  console.log('Windbreaker life.');
} else if (weather === 'rainy') {
  console.log('Bring that umbrella!');
} else if (weather === 'snowy') {
  console.log('Just stay inside!');
} else {
  console.log('Not a valid weather type');
}
```

5) Fix‑me mini‑exercises
- Correct each snippet so it runs and matches the comment.

```js
// 5a) Equality vs assignment — expect to print 'OK'
// if (x = 3) { console.log('OK'); }
let x = 3;
if (x === 3) { console.log('OK'); }

// 5b) Else pairing — expect only the greater message for 10
// if (10 > 5)
//   console.log('greater');
//   else
//   console.log('not greater');
if (10 > 5) {
  console.log('greater');
} else {
  console.log('not greater');
}

// 5c) Switch break — expect exactly one line for value 2
// const v = 2; switch (v) { case 1: console.log('one'); case 2: console.log('two'); default: console.log('other'); }
const v = 2;
switch (v) {
  case 1:
    console.log('one');
    break;
  case 2:
    console.log('two');
    break;
  default:
    console.log('other');
}
```

## Example Outputs

- If `day` is `Monday`, log: `Tomorrow is Tuesday`
- If `day` is `Sunday`, log: `Tomorrow is Monday`
- If `day` is `Moonday`, log: `Unrecognized day name`

## What to Submit

- The URL to your public CodePen `Ch. 3 - Conditions and Switch`.
- A short note that tasks 1–5 run and produce the expected messages.

## Grading (10 pts)

- Number classification with correct `if / else if / else` (2)
- Range check with `&&` and correct messages (2)
- Following day implemented with `switch`, `default`, and `break`s (4)
- Weather multiple choices with strict equality (1)
- Fix‑me mini‑exercises corrected (1)

## Tips & Troubleshooting

- Use strict comparison `===` / `!==` to avoid surprises.
- Be careful with braces so each `else` matches the intended `if`.
- In `switch`, missing `break` causes fall‑through into the next case.
