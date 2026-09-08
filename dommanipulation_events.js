// The DOM is the live representation of a web page. JavaScript reads and changes it.
// Events are the signals that tell JavaScript when to act.

// What the DOM is
// The DOM (Document Object Model) is a tree of objects that represents every element in an HTML page.
// The browser builds it when the page loads. 
// JavaScript can read from it, write to it, add new nodes, and remove existing ones.
// Every change to the DOM updates what the user sees instantly, without a page reload.

// selecting elements
// The first step in manipulating the DOM is to select the elements you want to work with.
// You can select elements by their tag name, class name, id, or other attributes.
// For example, to select an element with the id "myElement", you can use:
// const myElement = document.getElementById("myElement");

// You can also use querySelector and querySelectorAll for more complex selections:
// const firstParagraph = document.querySelector("p");
// const allButtons = document.querySelectorAll(".button-class");

// Once you have selected an element, you can read its properties, change its content, or modify its style.
// document.querySelector(selector) returns the first element that matches a CSS selector.
// document.querySelectorAll(selector) returns all matches as a NodeList.
// These are the two methods you will use for almost everything.

// Selector	                 Selects	                       Python equivalent
// #myId	          Element with id="myId"	              dict lookup by unique key
// .myClass	       All elements with class="myClass"	      list filter by attribute
// p	               All paragraph elements	              list filter by type
// div > span	    span elements directly inside a div	      nested dict access

// This page has a hidden element with id "d1target"
// Let's select it, read it, then change it

const el = document.querySelector('#d1target');

console.log("Tag name:", el.tagName);
console.log("Text content:", el.textContent);
console.log("Class list:", [...el.classList].join(', '));

// Change its content
el.textContent = "Updated by JavaScript";
console.log("New content:", el.textContent);

// Select all elements with class "d1item"
const items = document.querySelectorAll('.d1item');
console.log("\nNumber of .d1item elements:", items.length);

// Loop and read each one
items.forEach((item, index) => {
  console.log(`Item ${index}: ${item.textContent}`);
});

//Changing Content and Style
// You can change the content of an element using textContent or innerHTML.
// You can also change its style using the style property.

// Once you have a reference to an element, you can change what it displays and how it looks using three main properties: textContent, innerHTML, and style.

// Property	                                     What it does	                                  When to use
// el.textContent = "x"	                 Sets the visible text only	                When inserting plain text (safe)
// el.innerHTML = "<b>x</b>"	           Sets text including HTML tags	            When you need HTML formatting
// el.style.color = "red"	               Sets inline CSS on the element	            Dynamic style changes
// el.classList.add("active")	           Adds a CSS class	                          Toggle states via pre-written CSS
// el.classList.remove("active")	       Removes a CSS class	                      Toggle states via pre-written CSS

// Get the live display panel for this exercise
const panel = document.querySelector('#d2panel');

// Change text content
panel.textContent = "SMP Daily Report";
console.log("Set text:", panel.textContent);

// Change style properties
panel.style.color = "#4ecca3";
panel.style.fontWeight = "bold";
panel.style.padding = "8px";
panel.style.background = "#0a1628";
panel.style.borderRadius = "4px";
console.log("Styles applied");

// innerHTML adds HTML structure
panel.innerHTML = `
  <strong style="color:#f5a623;">Day 37</strong>
  | Steps: <span style="color:#4ecca3;">11,240</span>
  | Sleep: <span style="color:#a5d6ff;">7.5h</span>
  | Rating: <span style="color:#e94560;">Excellent</span>
`;
console.log("HTML injected into panel");

// Create a brand new element and append it
const newItem = document.createElement('p');
newItem.textContent = "Created by JavaScript at runtime";
newItem.style.color = "#8b949e";
newItem.style.fontSize = "0.85rem";
newItem.style.marginTop = "4px";
panel.appendChild(newItem);
console.log("New element appended");

// Tip: Use textContent when inserting user-provided text.
// It escapes HTML automatically, so a user who types <script>alert('x')</script> into a form cannot inject code.
// Use innerHTML only for HTML you write yourself and fully control.

// Events
// Events are signals that tell JavaScript when to act. 
// They can be triggered by user actions (clicks, typing, scrolling) or by the browser (page load, resize).
// You can listen for events on elements and run a function when they occur.
// An event is a signal the browser sends when something happens: a click, a keystroke, a form submission, a page load.
// addEventListener(eventName, callbackFunction) registers a function to run when that event fires on a specific element.

// Wire up the buttons in the live demo below
const addBtn    = document.querySelector('#d3addBtn');
const clearBtn  = document.querySelector('#d3clearBtn');
const logInput  = document.querySelector('#d3input');
const logList   = document.querySelector('#d3list');
const countEl   = document.querySelector('#d3count');

let count = 0;

addBtn.addEventListener('click', () => {
  const value = logInput.value.trim();
  if (!value) {
    console.log("No input to add.");
    return;
  }

  const today = new Date().toLocaleDateString();

  // Create new list item
  const li = document.createElement('li');
  li.textContent = `${today} - ${value}`;
  li.style.padding = "4px 0";
  li.style.borderBottom = "1px solid #30363d";
  logList.appendChild(li);

  count++;
  countEl.textContent = `Entries: ${count}`;
  logInput.value = "";
  logInput.focus();
  console.log(`Added: "${today} - ${value}"`);
});

clearBtn.addEventListener('click', () => {
  logList.innerHTML = "";
  count = 0;
  countEl.textContent = "Entries: 0";
  console.log("Log cleared.");
});

// Keyboard shortcut: Enter key submits
logInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    addBtn.click();
  }
});

console.log("Event listeners attached. Use the panel below.");

// Reading From Inputs
// You can read the value of an input field using the value property.
// For example, if you have an input element with id "myInput", you can get its value like this:
// const inputValue = document.getElementById("myInput").value;

// You can also listen for changes to the input using the 'input' or 'change' events.
// The 'input' event fires every time the user types or modifies the input.
// The 'change' event fires when the input loses focus after being modified.
// When a user fills out a form, JavaScript reads the values using element.value for text inputs and element.checked for checkboxes.
// The submit event fires when the form is submitted.
// Call event.preventDefault() to stop the browser from reloading the page.

// Wire up the SMP check-in form below
const form      = document.querySelector('#d4form');
const resultEl  = document.querySelector('#d4result');

form.addEventListener('submit', (event) => {
  event.preventDefault(); // Stop page reload

  // Read field values
  const name  = document.querySelector('#d4name').value.trim();
  const sleep = parseFloat(document.querySelector('#d4sleep').value);
  const water = parseInt(document.querySelector('#d4water').value);
  const steps = parseInt(document.querySelector('#d4steps').value);

  // Validate
  if (!name || isNaN(sleep) || isNaN(water) || isNaN(steps)) {
    resultEl.style.color = "#ff7b72";
    resultEl.textContent = "All fields are required.";
    return;
  }

  // Assess
  const hitGoal = steps >= 10000;
  const rating  = sleep >= 7.5 && water >= 8 && hitGoal ? "Excellent"
                : hitGoal                               ? "Good"
                : sleep >= 7.0                          ? "Average"
                : "Below target";

  // Display result
  resultEl.style.color = hitGoal ? "#4ecca3" : "#f5a623";
  resultEl.innerHTML = `
    <strong>${name}</strong>
    | Sleep: ${sleep}h | Water: ${water}gl | Steps: ${steps.toLocaleString()}
    | Goal: <strong>${hitGoal ? "HIT" : "MISS"}</strong>
    | Rating: <strong>${rating}</strong>
  `;

  console.log(`Check-in: ${name} | ${rating} | Goal: ${hitGoal ? "HIT" : "MISS"}`);
});

console.log("Form listener attached. Fill and submit the form below.");

//Tip: event.preventDefault() is one of the most important lines in front-end JavaScript.
// Without it, every form submit reloads the page and wipes your data.
// Call it as the first line inside any submit event listener.

