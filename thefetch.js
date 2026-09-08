//fetch(url) is a built-in browser function that sends an HTTP request to a URL and returns a Promise.
// A Promise is an object representing a value that is not available yet but will be resolved in the future.
// You use await to pause execution until the Promise resolves.

//Definition: async / await
//async marks a function as one that performs asynchronous work.
// Inside an async function, await pauses that function until the Promise it is waiting for resolves.
// The rest of the page keeps running while the wait happens.

// Basic Fetch Pattern
// The basic pattern for using fetch is to call fetch() with a URL, then use .then() to handle the response.
// You can also use async/await to make the code cleaner and easier to read.

// The full pattern every fetch request follows
/*
const fetchData = async () => {
  try {
    const response = await fetch("https://api.example.com/data");

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const data = await response.json(); // parse JSON body
    console.log(data);

  } catch (err) {
    console.error("Fetch failed:", err.message);
  }
};

fetchData();
*/
// Explanation of the code:
// 1. We define an asynchronous function called fetchData using the async keyword.
// 2. Inside the function, we use await to pause execution until the fetch() call resolves.
// 3. We check if the response is ok (status code in the range 200-299). If not, we throw an error.
// 4. We parse the JSON body of the response using response.json() and log it to the console.
// 5. We catch any errors that occur during the fetch or parsing process and log them to the console.

// Step	                      What happens	                       Python equivalent
// fetch(url)	           Sends the HTTP request	                requests.get(url)
// await response	       Waits for HTTP headers to arrive	        synchronous by default
// response.ok	           True if status is 200-299	            response.status_code == 200
// response.json()	       Parses the JSON body (async)	            response.json()
// try/catch	           Handles network errors	                try/except

// Simulate Fetch in the Browser:
// The terminals below use a simulated API that returns data instantly.
// The code structure is identical to what you use against a production API. The only difference is the URL.

// Note: Real fetch() calls hit a network endpoint.
// The simulated version here returns a resolved Promise containing hardcoded data, so you can practice the async/await pattern without needing a live server.

// Simulated fetch: returns same structure as a live API call
const simulatedFetch = async (endpoint) => {
  const db = {
    "/api/members": [
      { id: 1, name: "Brian Otieno",   city: "Nairobi",  protocol: "Phase 1" },
      { id: 2, name: "Wanjiku Muthoni",city: "Mombasa",  protocol: "Phase 2" },
      { id: 3, name: "Kamau Njoroge",  city: "Kisumu",   protocol: "Phase 1" },
      { id: 4, name: "Aisha Waweru",   city: "Nakuru",   protocol: "Phase 3" },
    ],
    "/api/stats": {
      totalMembers: 4,
      avgSteps: 10240,
      avgSleep: 7.3,
      goalHitRate: 0.68
    }
  };
  const data = db[endpoint];
  if (!data) throw new Error(`404: ${endpoint} not found`);
  return { ok: true, status: 200, json: async () => data };
};

// --- Use it exactly like fetch ---
const loadMembers = async () => {
  try {
    const response = await simulatedFetch("/api/members");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const members = await response.json();

    console.log(`Loaded ${members.length} members:\n`);
    members.forEach(m => {
      console.log(`  [${m.id}] ${m.name} | ${m.city} | ${m.protocol}`);
    });
  } catch (err) {
    console.log("Error:", err.message);
  }
};

const loadStats = async () => {
  try {
    const response = await simulatedFetch("/api/stats");
    const stats = await response.json();
    console.log("\nSMP Stats:");
    console.log(`  Members:      ${stats.totalMembers}`);
    console.log(`  Avg steps:    ${stats.avgSteps.toLocaleString()}`);
    console.log(`  Avg sleep:    ${stats.avgSleep}h`);
    console.log(`  Goal hit rate:${(stats.goalHitRate * 100).toFixed(0)}%`);
  } catch (err) {
    console.log("Error:", err.message);
  }
};

// Run both
await loadMembers();
await loadStats();


// POST Requests: Sending data to the server
// To send data to the server, you can use fetch() with the POST method.
// You need to include a body in the request, usually in JSON format, and set the appropriate headers.

// A POST request sends data to a server.
// Unlike GET (which only reads), POST creates or updates a resource.
// In JavaScript, you pass a second argument to fetch() with method: "POST", a body containing the JSON string, and headers declaring the content type.

// Simulated POST: mirrors fetch with method + body + headers
const simulatedPost = async (endpoint, payload) => {
  console.log(`POST ${endpoint}`);
  console.log("Payload sent:", JSON.stringify(payload, null, 2));
  // Server processes and responds
  const response = {
    success: true,
    memberId: Math.floor(Math.random() * 9000) + 1000,
    receivedAt: new Date().toISOString(),
    message: `Check-in for ${payload.name} recorded.`
  };
  return { ok: true, status: 201, json: async () => response };
};

// POST a daily check-in
const submitCheckIn = async (checkIn) => {
  try {
    const response = await simulatedPost("/api/checkin", checkIn);

    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const result = await response.json();

    console.log("\nServer response:");
    console.log(`  Success:   ${result.success}`);
    console.log(`  Member ID: ${result.memberId}`);
    console.log(`  Message:   ${result.message}`);
    console.log(`  Timestamp: ${result.receivedAt}`);
  } catch (err) {
    console.log("Error:", err.message);
  }
};

// What the fetch call looks like (VS Code)
/*
const response = await fetch("https://api.smp.com/checkin", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(checkIn)
});
*/

// Submit a check-in
const todayCheckIn = {
  name:  "Brian Otieno",
  date:  "2026-07-15",
  sleep: 7.5,
  water: 9,
  steps: 11240
};

await submitCheckIn(todayCheckIn);


// Fetch with DOM: Live Data Display
// You can use fetch() to get data and then display it in the DOM (the HTML page).
// This allows you to create dynamic web pages that update based on data from a server.

// Simulated member API
const simulatedFetch2 = async (endpoint) => {
  const members = [
    { name: "Brian Otieno",    city: "Nairobi",  steps: 11240, sleep: 7.5, goal: true },
    { name: "Wanjiku Muthoni", city: "Mombasa",  steps:  8900, sleep: 6.2, goal: false },
    { name: "Kamau Njoroge",   city: "Kisumu",   steps: 10050, sleep: 8.0, goal: true },
    { name: "Aisha Waweru",    city: "Nakuru",   steps: 12300, sleep: 7.8, goal: true },
    { name: "John Kimani",     city: "Eldoret",  steps:  7200, sleep: 5.9, goal: false },
  ];
  return { ok: true, json: async () => members };
};

// Target element in the demo panel below
const display = typeof document !== "undefined"
  ? document.querySelector('#f3display')
  : null;
const loadBtn = typeof document !== "undefined"
  ? document.querySelector('#f3loadBtn')
  : null;

const loadAndDisplay = async () => {
  display.textContent = "Loading...";
  display.style.color = "#f5a623";

  try {
    const response = await simulatedFetch2("/api/members");
    const members  = await response.json();

    // Build HTML table from data
    const rows = members.filter(m => m.goal).map(m => {
      const goalColor = m.goal ? "#4ecca3" : "#ff7b72";
      const goalText  = m.goal ? "HIT" : "MISS";
      return `<tr>
        <td style="color:#eaeaea;padding:6px 8px;">${m.name}</td>
        <td style="color:#a0a0b0;padding:6px 8px;">${m.city}</td>
        <td style="color:#a0a0b0;padding:6px 8px;">${m.steps.toLocaleString()}</td>
        <td style="color:#a0a0b0;padding:6px 8px;">${m.sleep}h</td>
        <td style="color:${goalColor};font-weight:700;padding:6px 8px;">${goalText}</td>
      </tr>`;
    }).join('');

    display.style.color = "inherit";
    display.innerHTML = `
      <table style="width:100%;border-collapse:collapse;font-size:0.85rem;">
        <thead>
          <tr style="background:#0f3460;">
            <th style="padding:6px 8px;text-align:left;">Name</th>
            <th style="padding:6px 8px;text-align:left;">City</th>
            <th style="padding:6px 8px;text-align:left;">Steps</th>
            <th style="padding:6px 8px;text-align:left;">Sleep</th>
            <th style="padding:6px 8px;text-align:left;">Goal</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    `;
    console.log(`Rendered ${members.length} members in the DOM.`);
  } catch (err) {
    display.textContent = "Error: " + err.message;
    display.style.color = "#ff7b72";
    console.log("Fetch failed:", err.message);
  }
};

// Wire the button when running in the browser
if (loadBtn && display) {
  loadBtn.addEventListener('click', loadAndDisplay);
  console.log("Click 'Load Members' in the panel below.");
}


// Same Pattern, Different Context: Fetching Dairy Farm Data
// The same async/await fetch pattern that loads SMP member records works for any remote dataset.
// Below is a simulated fetch of weekly milk yield records from a dairy farm API.
// The structure is the same: await the response, check response.ok, parse the JSON, loop through the data.

// Simulates: fetch("https://api.mwangifarm.co.ke/milk-records")
const fakeFetch = () => Promise.resolve({
  ok: true,
  json: () => Promise.resolve([
    { cow: "Daisy",   week: 1, litres: 98.5,  feed_kg: 50 },
    { cow: "Bella",   week: 1, litres: 112.0, feed_kg: 55 },
    { cow: "Kamau1",  week: 1, litres: 87.0,  feed_kg: 45 },
    { cow: "Daisy",   week: 2, litres: 105.0, feed_kg: 52 },
    { cow: "Bella",   week: 2, litres: 118.5, feed_kg: 57 },
  ])
});

const loadMilkRecords = async () => {
  try {
    const response = await fakeFetch();
    if (!response.ok) throw new Error("Server error");

    const records = await response.json();
    const totalLitres = records.reduce((sum, r) => sum + r.litres, 0);
    const avgPerCow   = totalLitres / records.length;

    console.log(`Records fetched: ${records.length}`);
    console.log(`Total litres: ${totalLitres.toFixed(1)}`);
    console.log(`Average per record: ${avgPerCow.toFixed(1)} L`);
    console.log("\nWeek 2 records:");
    records
      .filter(r => r.week === 2)
      .forEach(r => console.log(`  ${r.cow}: ${r.litres} L | feed ${r.feed_kg} kg`));
  } catch (err) {
    console.log("Fetch failed:", err.message);
  }
};

await loadMilkRecords();
