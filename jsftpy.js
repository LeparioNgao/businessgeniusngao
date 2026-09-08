// JavaScript runs in the browser. Python runs on a server. A REST API is the contract between them.
// JavaScript sends requests; Python processes and responds.

// The Architecture:

// A full-stack application has a front end (what the user sees in the browser) and a back end (logic and data running on a server).
// JavaScript handles the front end. Python handles the back end. They communicate via HTTP using JSON.

// Browser (JS)   --fetch()-->   Python API (FastAPI / Flask)   --query-->   
//            Database (Supabase / SQLite)
// Database   --data-->   Python API   --JSON-->   Browser (JS updates DOM)

// Request flows left to right. Response flows right to left. JSON is the data format in both directions.

// The Front End (JavaScript):

// The front end is the user interface. It runs in the browser and is built with HTML, CSS, and JavaScript.
// The browser sends fetch requests to the Python API.
// It does not know or care that Python is processing the request.
// It only knows the URL, the HTTP method, and the JSON structure of the response.

const API_BASE = "http://localhost:8000";

// GET all check-ins from Python API
const loadCheckIns = async () => {
  const response = await fetch(`${API_BASE}/api/checkins`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.json();
};

// POST a new check-in to Python API
const submitCheckIn = async (payload) => {
  const response = await fetch(`${API_BASE}/api/checkins`, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify(payload)
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.json();
};