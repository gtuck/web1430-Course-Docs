# Interview 01 Script — Chapters 1–5 (5 minutes)

- Duration: 5 minutes on Zoom (screen-share required)
- Scope: Ch. 1 (console, values/types, strings, arithmetic, sequence, comments), Ch. 2 (variables, assignment, Number, expressions), Ch. 3 (conditions), Ch. 4 (loops), Ch. 5 (functions)
- Format: Rapid Q&A + a small coding task solved live by the student

## Flow & Timing

- 0:00–0:15 Greeting and setup
  - Prompt: “Please share your screen in CodePen or your editor’s JS console.”
- 0:15–2:15 Concept Quickfire (6 short questions)
- 2:15–4:40 Live Coding Task (pick 1 variant)
- 4:40–5:00 Wrap‑up (brief reflection + scoring notes)

## Concept Quickfire (aim ~10–15s each)

1) Values & types
- Q: “What’s the difference between a number and a string in JS? Give one quick example of each.”
- Expected: number arithmetic vs string concatenation, e.g., 2 + 3 vs '2' + '3'.

2) Strings & quotes
- Q: “How do you include an apostrophe in a single‑quoted string?”
- Expected: escape with \\ or switch quote style.

3) Variables
- Q: “When would you use let vs const?”
- Expected: const for bindings that won’t be reassigned; let when reassignment is needed.

4) Conditions
- Q: “Why prefer === over ==?”
- Expected: strict equality avoids implicit type coercion surprises.

5) Loops
- Q: “Show a quick for loop counting 1..3.”
- Expected: for (let i=1; i<=3; i++) { ... }.

6) Functions
- Q: “What does a function return if there’s no return statement?”
- Expected: undefined.

## Live Coding Task (choose A or B)

A) describePerson function (recommended)
- Prompt: “Write a function describePerson(name, age) that returns 'Hello, Name! Next year you will be X (Y months).' If age >= 18, append ' Adult', else ' Minor'. Then call it once and console.log the result.”
- Acceptance:
  - Function with parameters, correct arithmetic (next year, months), conditional suffix, returns a string, logged once.
- Stretch (if time): “Use a loop to log numbers 1..age inclusive.”

B) greet + classify (fallback)
- Prompt: “Prompt for a name and age, convert age with Number, then log 'Hello, Name', and either 'Minor' or 'Adult' based on age (>= 18).”
- Acceptance: prompt/Number, if/else, console.log.

## Hints (offer only if stuck)

- “Remember to return from the function and then log the returned value.”
- “Number(age) converts prompt input from string to number.”
- “Use parentheses around (age + 1) when concatenating into strings.”

## Sample Solution (for instructor)

```js
function describePerson(name, age) {
  const next = age + 1;
  const months = age * 12;
  const status = age >= 18 ? ' Adult' : ' Minor';
  return 'Hello, ' + name + '! Next year you will be ' + next + ' (' + months + ' months).' + status;
}
console.log(describePerson('Ada', 17));
```

## Scoring (25 pts)

- Concept Quickfire (10)
  - Correct, concise answers across 6 prompts (10)
- Coding (12)
  - Function design & return value (4)
  - Arithmetic & string composition (4)
  - Conditional logic (>= 18) (2)
  - Clear logging + no runtime errors (2)
- Communication (3)
  - Thinks aloud, verifies with a quick run, responds to light guidance (3)

## Wrap‑Up Prompts (if time remains)

- “If you had 60 more seconds, what would you improve?”
- “One sentence on when you’d choose a while vs a for loop.”

