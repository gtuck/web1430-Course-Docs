# Assignment: Ch. 3 - Predict the final output - (in class assignment)

## Description

In a new [codepen.io](https://codepen.io/pen) named 'Predict output' using the code below. Before executing it, add your prediction in the comment block near the bottom for the final values of variables nb1, nb2, and nb3 depending on their initial values as indicated in the comment block at the top of the page.

## Objective

## Instructions

```
/*
Example inputs:
nb1=nb2=nb3=4			
nb1=4,nb2=3,nb3=2			
nb1=2,nb2=4,nb3=0
*/

let nb1 = Number(prompt("Enter nb1:"));
let nb2 = Number(prompt("Enter nb2:"));
let nb3 = Number(prompt("Enter nb3:"));

if (nb1 > nb2) {
  nb1 = nb3 * 2;
} else {
  nb1++;
  if (nb2 > nb3) {
    nb1 += nb3 * 3;
  } else {
    nb1 = 0;
    nb3 = nb3 * 2 + nb2;
  }
}

console.log(nb1, nb2, nb3);

/* Output prediction (replace ? with your prediction):
nb1=? nb2=? nb3=?
nb1=? nb2=? nb3=?
nb1=? nb2=? nb3=?
*/
```

## What to Submit

Submit the URL to your codepen.io