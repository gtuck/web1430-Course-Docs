Create a new codepen.io named "Discover the DOM." Your mission here is to complete the `showChild()` function that shows one of the children of a DOM element node. This function takes the parent node and the child node index as a parameter. Error cases like a non-element node or an out-of-limits index must be considered.

Here's the associated HTML code.

```
<h1>My web page</h1>
<p>Hello! My name's Baptiste.</p>
<p>I live in the great city of <a href="https://en.wikipedia.org/wiki/Bordeaux">Bordeaux</a>.</p>
```

Complete the following program to obtain the expected results.

```
// Show a DOM object's child node
// "node" is the DOM object
// "index" is the index of the child node
const showChild = (node, index) => {
  // TODO: add code here
};

// Should show the h1 node
showChild(document.body, 1);

// Should show "Incorrect index"
showChild(document.body, -1);

// Should show "Incorrect index"
showChild(document.body, 8);

// Should show "Wrong node type"
showChild(document.body.childNodes[0], 0);
```

> 

NOTE: Use console.error() rather than console.log() to display an error message in the console.
