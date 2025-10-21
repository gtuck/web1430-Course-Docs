# Assignment: Ch. 17 - Manipulate forms

## Description

In a new codepen.io named "Manipulate forms," add the provided HTML and CSS to the appropriate codepen.io tabs. Then, as described in the "[Coding time!](https://thejsway.net/chapter17/#coding-time)" section at the end of chapter 17 in our book, write the 3 Javascript functions to accomplish the tasks outlined.

---

## Objective

## Instructions

#### HTML:

```
 <h1>Forms</h1>

 <hr>

 <h2>Autocompletion</h2>
 <label for="country">Enter a country name</label>:
 <input type="text" id="country">
 <div id="suggestions"></div>

 <hr>

 <h2>A few of the Game of Thrones characters</h2>
 <form id="thrones">
 <label for="house">House</label>:
 <select name="house" id="house">
 <option value="" selected>Select a house</option>
 </select>
 </form>

 <p>
 <ul id="characters"></ul>
 </p>

 <hr>

 <h2>Password checker</h2>
 <form id="password">
 <p>
 <label for="password1">Enter the password</label>:
 <input type="password" name="password1" id="password1" required>
 </p>
 <p>
 <label for="password2">Confirm the password</label>:
 <input type="password" name="password2" id="password2" required>
 </p>

 <input type="submit" value="Send">
 </form>

 <p id="passwordHelp"></p>
```

#### CSS:

```
/* Add spacing between each country suggestion */
.suggestion {
    padding-left: 2px;
    padding-right: 2px;
}

/* Change suggestion color when hovering it with the mouse */
.suggestion:hover {
    background-color: #adf;
    cursor: pointer;
}

/* Position the suggestion list just below the input box */
#suggestions {
    position: absolute;
    border: 1px solid black;
    left: 155px;
    background: #fff;
}
```

#### Add JavaScript to accomplish the following tasks as described in the book:

1. autocompletion
2. got_characters
3. password_checker

---

## What to Submit

Please submit the URL to your codepen.io