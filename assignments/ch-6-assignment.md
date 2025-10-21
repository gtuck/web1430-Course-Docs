# Ch. 6 Assignment: Objects Lab — Create Your First Objects

## Description

Practice Chapter 6 fundamentals: create object literals, read/update properties with dot notation, add properties dynamically, define methods that use `this`, and model simple real‑world entities. You’ll build four small tasks in one CodePen: Aurora with XP, a dog, a circle, and a bank account.

## Learning Objectives

- Create object literals with key/value properties.
- Access and modify properties via dot notation.
- Add new properties after object creation.
- Define methods and use `this` to access the current object.
- Convert user input with `Number()` when needed.
- Log clean, descriptive output with `console.log()`.

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 6 - Objects Lab`.
- Use the JS panel only (no HTML/CSS).
- Open the CodePen Console (click `Console` at the bottom).
- Optional: Pen Settings → Behavior → enable “Clear Console on Run”.

## Instructions

Work top‑to‑bottom in the JS panel. Add comments to separate tasks.

1) Adding character experience (Aurora)
- Create an `aurora` object with properties: `name: "Aurora"`, `health: 150`, `strength: 25`.
- Add a `describe()` method that returns a string including name, health, strength, and XP (use `this`).
- Add a new property `xp` initialized to `0` (can be in the literal or added after).
- Then apply updates in order and print the description:
  - Aurora is harmed by an arrow → `health -= 20`
  - Aurora equips a strength necklace → `strength += 10`
  - Aurora learns a new skill → `xp += 15`

```js
// 1) Aurora with XP and describe()
const aurora = {
  name: 'Aurora',
  health: 150,
  strength: 25,
  xp: 0,
  describe() {
    return `${this.name} has ${this.health} health points, ${this.strength} as strength and ${this.xp} XP points`;
  }
};

// updates
aurora.health -= 20; // harmed by an arrow
aurora.strength += 10; // strength necklace
aurora.xp += 15; // new skill

console.log(aurora.describe());
// e.g., "Aurora has 130 health points, 35 as strength and 15 XP points"
```

2) Modeling a dog
- Create a `dog` object with properties: `name` (your choice), `species` (e.g., 'boarhound'), `size` (a number).
- Add a `bark()` method that returns a bark string (e.g., `'Grrr! Grrr!'`).
- Log the two lines shown below.

```js
// 2) Dog object with a bark() method
const dog = {
  name: 'Fang',
  species: 'boarhound',
  size: 75,
  bark() {
    return 'Grrr! Grrr!';
  }
};

console.log(`${dog.name} is a ${dog.species} dog measuring ${dog.size}`);
console.log(`Look, a cat! ${dog.name} barks: ${dog.bark()}`);
```

3) Modeling a circle
- Ask the user for a radius value, then build a `circle` object with that radius.
- Add methods `circumference()` and `area()` that compute values using `Math.PI` and `this.radius`.
- Log the circumference and area lines below.

```js
// 3) Circle object with methods
const r = Number(prompt('Enter the circle radius:'));
const circle = {
  radius: r,
  circumference() {
    return 2 * Math.PI * this.radius;
  },
  area() {
    return Math.PI * this.radius * this.radius; // or this.radius ** 2
  }
};

console.log(`Its circumference is ${circle.circumference()}`);
console.log(`Its area is ${circle.area()}`);
```

4) Modeling a bank account
- Create an `account` object with:
  - `name` set to `'Alex'`
  - `balance` set to `0`
  - `credit(amount)` method that adds the passed value to `balance` (supports negatives for debits)
  - `describe()` method returning a description string
- Use it to log the description, credit 250, debit 80 (by passing `-80`), then log the description again.

```js
// 4) Bank account object
const account = {
  name: 'Alex',
  balance: 0,
  credit(amount) {
    this.balance += amount;
  },
  describe() {
    return `Owner: ${this.name}, balance: ${this.balance}`;
  }
};

console.log(account.describe());
account.credit(250);
account.credit(-80);
console.log(account.describe());
```

## Example Outputs

- Aurora: `Aurora has 130 health points, 35 as strength and 15 XP points`
- Dog: `Fang is a boarhound dog measuring 75` then `Look, a cat! Fang barks: Grrr! Grrr!`
- Circle: `Its circumference is 18.8495...` and `Its area is 28.2743...` for radius 3
- Account: `Owner: Alex, balance: 0` then `Owner: Alex, balance: 170`

## What to Submit

- The URL to your public CodePen `Ch. 6 - Objects Lab`.
- A short note that tasks 1–4 run and produce the expected messages.

## Grading (25 pts)

- Aurora object with `xp` and working `describe()` using `this` (8)
- Dog object with `bark()` and correct logs (5)
- Circle object with `circumference()` and `area()` using `Math.PI` (5)
- Account object with `credit()` and `describe()`, correct before/after (5)
- Clear, readable console output (2)

## Tips & Troubleshooting

- Use `this.property` inside methods to access the current object.
- You can add new properties after creation (e.g., `obj.newProp = value`).
- Convert prompt input with `Number()` for numeric math.
- Template literals (backticks) make string building easier, but string concatenation works too.
