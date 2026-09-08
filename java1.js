// JavaScript fundamentals

// Variables
const name = "Brian";
const age = 28;

// Output to the browser console
console.log(`Name: ${name}, Age: ${age}`);

// A simple function
function greet(person) {
  return `Hello, ${person}!`;
}

console.log(greet("Alice"));

// Variables: let and const

// const declares a variable that will not be reassigned.
// let declares a variable that may be reassigned later. Use const by default.
// Switch to let only when you know the value will change.

// Keyword	 Reassignable?	    Use case
// const	        No	       Configuration, names, fixed data
// let	        Yes	           Counters, running totals, loop variables
// var	        Yes	           Old code only. Avoid in new code.

// const for fixed values
const athleteName = "Brian Otieno";
const protocol = "SMP Phase 1";
const targetSteps = 10000;

// let for values that change
let dayNumber = 1;
let stepCount = 0;

console.log("Athlete:", athleteName);
console.log("Protocol:", protocol);
console.log("Target steps:", targetSteps);

// Reassign let variable
dayNumber = 7;
stepCount = 11240;

console.log("\nDay:", dayNumber);
console.log("Steps logged:", stepCount);
console.log("Hit goal:", stepCount >= targetSteps);

// typeof checks the data type
console.log("\nTypes:");
console.log("athleteName:", typeof athleteName);   // string
console.log("targetSteps:", typeof targetSteps);   // number
console.log("hit goal:",    typeof true);           // boolean

// Strings and Template Literals.

// A template literal is a string that uses backticks instead of quotes and can embed variables directly using ${variable}.
// This is JavaScript's equivalent of Python's f-strings.

const name2 = "Kamau";
const sleep = 7.5;
const steps = 12340;
const goal = 10000;

// Template literal: backticks + ${}
const report = `Athlete: ${name}
Sleep:   ${sleep} hours
Steps:   ${steps.toLocaleString()}
Goal:    ${goal.toLocaleString()}
Result:  ${steps >= goal ? "HIT" : "MISS"}`;

console.log(report);

// String methods
const city = "  nairobi  ";
console.log("\nRaw city:", `"${city}"`);
console.log("Trimmed:", `"${city.trim()}"`);
console.log("Upper:", city.trim().toUpperCase());
console.log("Length:", city.trim().length);

// String includes and startsWith
const skill = "phone repair";
console.log("\nIncludes 'repair':", skill.includes("repair"));
console.log("Starts with 'phone':", skill.startsWith("phone"));
console.log("Replace:", skill.replace("phone", "laptop"));

// Arrays
// An array is an ordered list of values.
// In JavaScript, arrays use square brackets and are equivalent to Python lists.
// Items are accessed by index starting at zero.

// SMP skills list
const skills = ["welding", "tiling", "copywriting", "phone repair", "beekeeping"];

console.log("Skills:", skills);
console.log("First:", skills[0]);
console.log("Last:", skills[skills.length - 1]);
console.log("Count:", skills.length);

// Add and remove items
skills.push("plumbing");          // add to end
const removed = skills.shift();  // remove from front
console.log("\nAfter push + shift:", skills);
console.log("Removed:", removed);

// Array methods that return new arrays
const stepLog = [8200, 11400, 6300, 10050, 9800, 12100, 7500];

const hitDays = stepLog.filter(s => s >= 10000);
const doubled = stepLog.map(s => s * 2);
const total   = stepLog.reduce((sum, s) => sum + s, 0);
const average = total / stepLog.length;

// Spread creates a copy so the original array stays unchanged.
// Sorting numbers needs a compare function; default sort would treat numbers as strings.
const sorted = [...stepLog].sort((a, b) => b - a);

console.log("\nStep log:", stepLog);
console.log("Sorted step log:", sorted);
console.log("Hit days (>=10k):", hitDays);
console.log("Total steps:", total.toLocaleString());
console.log("Average:", Math.round(average).toLocaleString());

// Check membership
console.log("\nIncludes 6300:", stepLog.includes(6300));
console.log("Index of 9800:", stepLog.indexOf(9800));

// Objects
// An object is a collection of key-value pairs.
// In JavaScript, objects use curly braces and are equivalent to Python dictionaries.
// Keys are strings. Values can be any type, including other objects or arrays.

// SMP member object
const member = {
  name3: "Wanjiku Muthoni",
  city2: "Nairobi",
  protocol: "SMP Phase 2",
  weeksCompleted: 4,
  skills: ["copywriting", "social media"],
  stats: {
    avgSleep: 7.2,
    avgSteps: 9800,
    goalHitRate: 0.71
  }
};

// Access with dot notation
console.log("Name:", member.name);
console.log("City:", member.city);
console.log("Weeks done:", member.weeksCompleted);

// Access nested object
console.log("Avg sleep:", member.stats.avgSleep);
console.log("Goal hit rate:", `${(member.stats.goalHitRate * 100).toFixed(0)}%`);

// Access array inside object
console.log("Skills:", member.skills.join(", "));

// Add a new key
member.lastActive = "2026-07-14";
console.log("\nLast active:", member.lastActive);

// Destructure to pull out named keys
const { name3, city2, weeksCompleted } = member;
console.log(`\n${name} | ${city} | Week ${weeksCompleted}`);

// Object.keys and Object.entries
console.log("\nTop-level keys:", Object.keys(member));

// Functions
// A function is a reusable block of code.
// JavaScript has two common ways to write functions: function declarations and arrow functions.
// Arrow functions are shorter and are standard in modern JavaScript.

// Python
// def assess_day(steps, goal=10000):
//     if steps >= goal:
//        return "HIT"
//     return "MISS"

// JavaScript (arrow function)
//const assessDay = (steps, goal = 10000) => {
 // if (steps >= goal) return "HIT";
 // return "MISS";
//};

// Arrow function with default parameter
const assessDay = (steps, goal = 10000) => {
  if (steps >= goal) return "HIT";
  return "MISS";
};

// Function returning an object
const analyzeDay = (sleep, water, steps) => {
  const hitGoal = steps >= 10000;
  let rating;
  if (sleep >= 7.5 && water >= 8 && hitGoal) {
    rating = "Excellent";
  } else if (hitGoal) {
    rating = "Good";
  } else if (sleep >= 7.0) {
    rating = "Average";
  } else {
    rating = "Below target";
  }
  return { sleep, water, steps, hitGoal, rating };
};

// Test with SMP data
const days = [
  [8.0, 10, 12100],
  [5.5,  4,  7800],
  [7.2,  8, 10050],
  [6.0,  5,  9200],
];

days.forEach(([sleep, water, steps]) => {
  const result = analyzeDay(sleep, water, steps);
  console.log(`Sleep:${result.sleep}h  Water:${result.water}gl  Steps:${result.steps.toLocaleString()}  --> ${result.rating}`);
});

// for...of loop
console.log("\nGoal assessments:");
const stepLog1 = [9800, 11400, 6300, 10050];
for (const steps of stepLog1) {
  console.log(`  ${steps.toLocaleString()} --> ${assessDay(steps)}`);
}

// Function returning an object with total, average, and hitCount
function weekSummary(stepCounts) {
  const total = stepCounts.reduce((sum, value) => sum + value, 0);
  const average = total / stepCounts.length;
  const hitCount = stepCounts.filter(value => value >= 10000).length;

  return {
    total,
    average,
    hitCount
  };
}

const summary = weekSummary(stepLog1);
console.log("\nWeek summary:", summary);

// Key Differences from Python
// Feature	              Python	                   JavaScript
// Semicolons	         Not used	              Optional but recommended
// Indentation	        Required (syntax)	      Optional (style only)
// Blocks	            Colon + indent	          Curly braces {}
// String format	    f"hello {name}"	          `hello ${name}`
// Null check	        if x is None	          if (x === null || x === undefined)
// List	                   []	                  [] (array)
// Dictionary	           {}	                  {} (object)
// Print	             print()	              console.log()
// Function	             def name():	          const name = () => {}
// Strict equality	        ==	                   === (type + value)

// Note on ===: JavaScript has two equality operators.
// == does type coercion ("5" == 5 is true).
// === checks both type and value ("5" === 5 is false).
// Always use === in your code.
