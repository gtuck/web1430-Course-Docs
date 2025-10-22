# Ch. 9 Assignment: OOP Lab — Classes, Methods, RPG

## Description

Practice Chapter 9 OOP by defining ES6 classes with constructors and methods, using `this`, instantiating with `new`, and managing state changes. Build three small programs in one CodePen: a `Dog` class, an RPG `Character` class with combat (plus inventory), and an `Account` list managed in an array.

## Learning Objectives

- Define classes with `class`, `constructor`, and methods.
- Use `this` correctly inside methods to access instance data.
- Instantiate with `new` and manage instance state changes.
- Compose objects in arrays and iterate over them.
- Extend behavior (e.g., transfer inventory on defeat) cleanly inside methods.

## Setup (CodePen Only)

- Create a new CodePen named `Ch. 9 - OOP Lab`.
- Use the JS panel only (no HTML/CSS).
- Open the CodePen Console (click `Console` at the bottom).
- Optional: Pen Settings → Behavior → enable “Clear Console on Run”.

## Instructions

Work top‑to‑bottom in the JS panel. Comment sections clearly.

1) Dogs — class and method
- Define a `Dog` class with `name`, `species`, `size` (set in the constructor) and a `bark()` method.
- Dogs taller than 60 bark `"Grrr! Grrr!"`; other dogs bark `"Woof! Woof!"`.
- Create two dogs and log the lines shown.

```js
// 1) Dog class
class Dog {
  constructor(name, species, size) {
    this.name = name;
    this.species = species;
    this.size = size;
  }
  bark() {
    return this.size > 60 ? 'Grrr! Grrr!' : 'Woof! Woof!';
  }
}

const fang = new Dog('Fang', 'boarhound', 75);
console.log(`${fang.name} is a ${fang.species} dog measuring ${fang.size}`);
console.log(`Look, a cat! ${fang.name} barks: ${fang.bark()}`);

const snowy = new Dog('Snowy', 'terrier', 22);
console.log(`${snowy.name} is a ${snowy.species} dog measuring ${snowy.size}`);
console.log(`Look, a cat! ${snowy.name} barks: ${snowy.bark()}`);
```

2) RPG — Character class with combat
- Create a `Character` class with properties `name`, `health`, `strength`, and `xp` (start at 0). Add methods:
  - `attack(target)` that applies damage and awards 10 XP on elimination.
  - `describe()` that returns a description string.
- Instantiate two heroes and a monster, then run the sample sequence.

```js
// 2) RPG Character class
class Character {
  constructor(name, health, strength) {
    this.name = name;
    this.health = health;
    this.strength = strength;
    this.xp = 0; // XP starts at 0
    // Inventory for step 3
    this.gold = 10;
    this.keys = 1;
  }
  // Attack a target
  attack(target) {
    if (this.health > 0) {
      const damage = this.strength;
      console.log(`${this.name} attacks ${target.name} and causes ${damage} damage points`);
      target.health -= damage;
      if (target.health > 0) {
        console.log(`${target.name} has ${target.health} health points left`);
      } else {
        target.health = 0;
        const bonusXP = 10;
        console.log(`${this.name} eliminated ${target.name} and wins ${bonusXP} experience points`);
        this.xp += bonusXP;
        // Step 3: transfer inventory on defeat
        if (typeof target.gold === 'number' && typeof target.keys === 'number') {
          this.gold += target.gold;
          this.keys += target.keys;
          target.gold = 0;
          target.keys = 0;
        }
      }
    } else {
      console.log(`${this.name} can’t attack (they've been eliminated)`);
    }
  }
  // Return the character description
  describe() {
    return `${this.name} has ${this.health} health points, ${this.strength} as strength and ${this.xp} XP points (inventory: ${this.gold} gold, ${this.keys} key(s))`;
  }
}

console.log('Welcome to the adventure! Here are our heroes:');
const aurora = new Character('Aurora', 150, 25);
const glacius = new Character('Glacius', 130, 30);
console.log(aurora.describe());
console.log(glacius.describe());

const monster = new Character('Spike', 40, 20);
console.log("A wild monster has appeared: it's named " + monster.name);

monster.attack(aurora);
monster.attack(glacius);
aurora.attack(monster);
glacius.attack(monster);

console.log(aurora.describe());
console.log(glacius.describe());
```

3) Character inventory (builds on step 2)
- Ensure each character has an inventory: `gold` and `keys` (initialized to 10 and 1).
- Inventory appears in `describe()`.
- When a character eliminates another, transfer the victim’s inventory to the vanquisher (implemented above inside `attack`).
- Verify after the monster is defeated that the winner’s gold/keys increased.

4) Account list — classes and arrays
- Define an `Account` class with:
  - `name` (string)
  - `balance` (starts at 0)
  - `credit(amount)` that adds amount (positive or negative) to balance
  - `describe()` that returns `Owner: <name>, balance: <balance>`
- Create three accounts: Sean, Brad, Georges; store in an array; credit 1000 to each; log each description.

```js
// 4) Account list
class Account {
  constructor(name) {
    this.name = name;
    this.balance = 0;
  }
  credit(amount) {
    this.balance += amount;
  }
  describe() {
    return `Owner: ${this.name}, balance: ${this.balance}`;
  }
}

const accounts = [new Account('Sean'), new Account('Brad'), new Account('Georges')];
accounts.forEach(acc => acc.credit(1000));
accounts.forEach(acc => console.log(acc.describe()));
```

## Example Outputs

- Dog:
  - `Fang is a boarhound dog measuring 75` then `Look, a cat! Fang barks: Grrr! Grrr!`
  - `Snowy is a terrier dog measuring 22` then `Look, a cat! Snowy barks: Woof! Woof!`
- RPG (sample):
  - Matches the chapter’s sequence, ending with heroes’ XP and inventory displayed.
- Accounts:
  - `Owner: Sean, balance: 1000`
  - `Owner: Brad, balance: 1000`
  - `Owner: Georges, balance: 1000`

## What to Submit

- The URL to your public CodePen `Ch. 9 - OOP Lab`.
- A short note that tasks 1–4 run and produce the expected messages.

## Grading (25 pts)

- Dog class with correct `bark()` behavior and logs (6)
- Character class: combat flow with `attack()` and `describe()` (8)
- Inventory added: appears in description and transfers on defeat (8)
- Account class: array of accounts credited and described (3)

## Tips & Troubleshooting

- Use `this` inside methods to access instance fields.
- Keep combat logic in `attack()` so side effects (XP, inventory) are centralized.
- Prefer template literals for readable output.
- Arrays make it easy to manage multiple objects (e.g., accounts).
