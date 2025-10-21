# Ch. 1 Assignment: Console Skills: Quotes, Math, and Messages

## Description

Practice the core JavaScript skills from Chapter 1: sending messages with `console.log()`, working with values and types (numbers and strings), using quotes for strings, performing basic arithmetic, concatenating strings, understanding sequential execution, and writing comments. You’ll build a small script that prints information about you and performs a few simple calculations.

## Learning Objectives

- Use `console.log()` to display messages in the console.
- Distinguish number vs. string values.
- Create strings using one quote style consistently; escape same‑quote characters with `\`.
- Perform arithmetic with `+`, `-`, `*`, and `/` on numbers.
- Concatenate strings with `+` (strings only).
- Observe that code runs top‑to‑bottom (sequential execution).
- Add explanatory comments with `//` and `/* ... */`.

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 1 - My Name Is`.
- Write all code in the JS panel.
- Open the CodePen Console (click `Console` at the bottom bar) to view `console.log()` output.
- Optional: In Pen Settings → Behavior, disable “Auto-Updating Preview” so output only runs when the `Run` button is clicked.

## Instructions

Work through the steps below in the JS panel. Keep all code in one place so it runs from top to bottom. Add comments to separate each section. Do not use variables yet — only values, expressions, and `console.log()`.

1) Hello, console
- Print a simple starter message.

```js
// 1) Hello, console
console.log('Starting Chapter 1 assignment...');
```

2) Your basic info (values and types)
- Log your first name (as a string value) and your age (as a number value). Replace the examples with your own info.

```js
// 2) Your basic info (values and types)
console.log('YourFirstName'); // string — replace with your name
console.log(20);              // number — replace with your age
```

3) Strings and quotes
- Use one quote style consistently (we’ll use single quotes here). If you need an apostrophe inside, escape it with `\`.

```js
// 3) Strings and quotes
console.log('My favorite book is "Dune".');
console.log('It\'s a great read.');
```

4) Arithmetic with numbers
- Using your age number, compute and log (replace 20 with your age):
  - Your age next year (20 + 1)
  - Your age in months (20 * 12)
  - Half your age (20 / 2)
  - A difference and a product of two numbers of your choice

```js
// 4) Arithmetic with numbers (replace 20 with your age)
console.log('Next year age:');
console.log(20 + 1);
console.log('Age in months:');
console.log(20 * 12);
console.log('Half age:');
console.log(20 / 2);
console.log('Difference 10 - 3 =');
console.log(10 - 3);
console.log('Product 9 * 7 =');
console.log(9 * 7);
```

5) String concatenation
- Build friendly messages by joining strings with `+` (strings only).

```js
// 5) String concatenation (replace with your info)
console.log('Hello, ' + 'YourFirstName' + '!');
console.log('You are ' + '20' + ' years old.');
console.log('Next year you will be ' + '21' + ' years old.');
```

6) Sequential execution
- Predict the output order in a comment, then run and compare. Notice how order matters even without variables.

```js
// 6) Sequential execution
// Prediction: Line A, then Line B, then Line C (top to bottom)
console.log('Line A');
console.log('Line B');
console.log('Line C');
```

7) Comments
- Add one‑line comments (`// ...`) and a multi‑line block (`/* ... */`) explaining what your code does.

```js
// 7) Comments
// This section summarizes what we printed above.
/*
  We practiced:
  - console.log()
  - strings and numbers
  - arithmetic and concatenation
  - execution order and comments
*/
console.log('Summary complete.');
```

8) Fix‑me mini‑exercises
- Fix each line so it runs and prints the intended message.

```js
// 8) Fix‑me mini‑exercises
// a) Quote mismatch — should print: Name: <your name>
// console.log("Name: ' + 'YourFirstName);
console.log('Name: ' + 'YourFirstName');

// b) Arithmetic precedence — should print a correct next‑year age as a number
// console.log('Age next year: ' + 20 + 1);
console.log('Age next year:');
console.log(20 + 1);

// c) Quotes inside quotes — should print: He said, "It's fine."
// console.log('He said, "It's fine."');
console.log('He said, "It\'s fine."');
```

## Example Outputs

Your exact output will vary, but you should see a series of lines similar to:

```
Starting Chapter 1 assignment...
YourFirstName
20
My favorite book is "Dune".
It's a great read.
Next year age:
21
Age in months:
240
Half age:
10
Difference 10 - 3 =
7
Product 9 * 7 =
63
Hello, YourFirstName!
You are 20 years old.
Next year you will be 21 years old.
Line A
Line B
Line C
Summary complete.
Name: YourFirstName
Age next year: 21
He said, "It's fine."
```

## What to Submit

- The URL to your public CodePen `Ch. 1 - My Name Is`.
- A note in the Pen description that your console shows the required output.

## Grading (25 pts)

- Uses `console.log()` appropriately (2)
- Demonstrates number and string values (2)
- Uses one quote style consistently and escapes same‑quote characters (5)
- Performs arithmetic with `+`, `-`, `*`, `/` (5)
- Concatenates strings with `+` (strings only) (3)
- Demonstrates sequential execution by ordering outputs (3)
- Includes both `//` and `/* ... */` comments (3)
- Fix‑me mini‑exercises corrected (2)

## Tips & Troubleshooting

- If you get a syntax error, check for missing quotes, mismatched parentheses, or stray commas.
- Use the same quote style throughout your Pen.
- When in doubt, log intermediate results with `console.log()` to verify your reasoning.
