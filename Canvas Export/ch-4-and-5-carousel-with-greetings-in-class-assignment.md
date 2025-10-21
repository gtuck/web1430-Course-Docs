# Assignment: Ch. 4 & 5 - Carousel with Greetings - (in class assignment)

## Description

## Objective

![](https://educalingo.com/en/dic-en/carousel)![carousel.jpg]($IMS-CC-FILEBASE$/Uploaded%20Media/carousel.jpg)![](https://educalingo.com/en/dic-en/carousel)

Create an interactive program that simulates a carousel ride. For each carousel turn, the rider will randomly greet the user using one of three different greeting functions. This exercise will help you practice working with variables, loops, conditional statements, and functions.

## Instructions

1. **Set Up Your Workspace:**

  - Create a new project on [codepen.io](https://codepen.io) titled **Carousel Greetings**.

2. **Program Overview:**

  - Your program will prompt the user to enter two pieces of information: 

    - The number of turns the carousel should take.
    - The rider's name.

  - For each turn of the carousel, display the current turn number and a random greeting message from the rider.

3. **Step-by-Step Guide:**

  - **Step 1:** Prompt the user to enter the number of turns the carousel should make. Store this value in a variable.

```
const turns = Number(prompt("Enter the number of turns for the carousel:"));
```

  - **Step 2:** Prompt the user to enter the rider's name. Store this value in another variable.

```
const riderName = prompt("Please enter the rider's name:");
```

  - **Step 3:** Create three greeting functions using different function types:

    - `sayHello1`: Create this function using a **function declaration**.
    - `sayHello2`: Create this function using a **function expression (anonymous function)**.
    - `sayHello3`: Create this function using an **arrow function**.
    - Each function should take a single parameter (the rider's name) and return a unique greeting message using that name.

```
// Function declaration
function sayHello1(name) {
    return `Hello, ${name}! Welcome to the carousel!`;
}

// Function expression / anonymous function
const sayHello2 = function(name) {
    return `Hi there, ${name}! Enjoy the ride!`;
};

// Arrow function
const sayHello3 = (name) => `Greetings, ${name}! Hope you're having fun!`;
```

  - **Step 4:** Use a `for` loop to simulate the carousel turning for the specified number of turns:

    - Inside the loop, use a random number generator to select one of the three greeting functions without using an array.
    - Display both the current turn number and the selected greeting message.

```
for (let i = 1; i <= turns; i++) {
    // Choose a random number between 1 and 3
    const randomChoice = Math.floor(Math.random() * 3) + 1;
    let greetingMessage;

    // Use if-else or switch statement to select the appropriate function
    if (randomChoice === 1) {
        greetingMessage = sayHello1(riderName);
    } else if (randomChoice === 2) {
        greetingMessage = sayHello2(riderName);
    } else if (randomChoice === 3) {
        greetingMessage = sayHello3(riderName);
    }

    // Output the turn number and the greeting
    console.log(`This is turn number ${i}`);
    console.log(greetingMessage);
}
```

4. **Output Requirements:**

  - For each turn, the program should display two lines in the console: 

    1. `This is turn number X` (where `X` is the current turn number).
    2. A greeting message from one of the three greeting functions, using the rider's name.

**Example Output:**

```
This is turn number 1
Hi there, Alice! Enjoy the ride!
This is turn number 2
Greetings, Alice! Hope you're having fun!
This is turn number 3
Hello, Alice! Welcome to the carousel!
```

5. **Testing Your Code:**

  - Test your program with different numbers of turns and different rider names to ensure it works as expected.
  - Refresh your codepen.io page to reset the prompts and try new inputs.

## What to Submit

  - Save your CodePen project and submit the link.