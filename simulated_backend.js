// === Simulated Python Backend ===
const pythonBackend = {
  checkins: [],

  GET: async (path) => {
    if (path === "/api/checkins") {
      return { status: 200, body: pythonBackend.checkins };
    }
    if (path.startsWith("/api/checkins/")) {
      const name = decodeURIComponent(path.split("/")[3]);
      const records = pythonBackend.checkins.filter(c => c.name === name);
      if (!records.length) return { status: 404, body: { error: "Not found" } };
      return { status: 200, body: records };
    }
    return { status: 404, body: { error: "Route not found" } };
  },

  POST: async (path, payload) => {
    if (path === "/api/checkins") {
      const entry = {
        ...payload,
        hit_goal: payload.steps >= 10000,
        rating:   payload.sleep >= 7.5 && payload.water >= 8 && payload.steps >= 10000
                    ? "Excellent"
                    : payload.steps >= 10000 ? "Good" : "Below target",
        id: pythonBackend.checkins.length + 1
      };
      pythonBackend.checkins.push(entry);
      return { status: 201, body: { success: true, entry } };
    }
    return { status: 404, body: { error: "Route not found" } };
  }
};

// Adapter: makes pythonBackend look like fetch()
const apiFetch = async (path, options = {}) => {
  const method = (options.method || "GET").toUpperCase();
  const payload = options.body ? JSON.parse(options.body) : undefined;
  const result  = method === "POST"
    ? await pythonBackend.POST(path, payload)
    : await pythonBackend.GET(path);
  return { ok: result.status < 400, status: result.status, json: async () => result.body };
};

// === JavaScript Frontend ===
const submitCheckIn = async (data) => {
  const res = await apiFetch("/api/checkins", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
};

const loadCheckIns = async () => {
  const res = await apiFetch("/api/checkins");
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
};

// Keep the demo compatible with Node's default CommonJS mode.
(async () => {
  // Submit four check-ins
  const entries = [
    { name: "Brian Otieno",    sleep: 8.0, water: 10, steps: 12100 },
    { name: "Wanjiku Muthoni", sleep: 5.5, water:  4, steps:  7800 },
    { name: "Kamau Njoroge",   sleep: 7.5, water:  9, steps: 10050 },
    { name: "GitHub Copilot",  sleep: 8.0, water:  8, steps: 11000 },
  ];

  for (const entry of entries) {
    const result = await submitCheckIn(entry);
    console.log(`POST /api/checkins --> 201`);
    console.log(`  Stored: ${result.entry.name} | Goal: ${result.entry.hit_goal ? "HIT" : "MISS"} | Rating: ${result.entry.rating}`);
  }

  // Load all
  console.log("\nGET /api/checkins --> 200");
  const all = await loadCheckIns();
  console.log(`  Total records: ${all.length}`);
  all.forEach(c => {
    console.log(`  [${c.id}] ${c.name} | ${c.rating}`);
  });

  // Load only entries that hit the step goal
  console.log("\nGET /api/checkins?hit_goal=true --> 200");
  const goalHitEntries = all.filter(c => c.hit_goal);
  console.log(`  Goal-hit records: ${goalHitEntries.length}`);
  goalHitEntries.forEach(c => {
    console.log(`  [${c.id}] ${c.name} | ${c.rating}`);
  });
})();

// CORS: Why it exists and how to handle it in a real backend
// In a real backend, you would need to handle CORS (Cross-Origin Resource Sharing) if your frontend and backend are on different origins.
// This typically involves setting appropriate HTTP headers in the backend responses, such as "Access-Control-Allow-Origin".
// In this simulated backend, we don't have to worry about CORS since everything is running in the same environment.

 // Definition: CORS
// CORS (Cross-Origin Resource Sharing) is a browser security policy that blocks JavaScript from making requests to a different domain than the page it is on.
// If your HTML file is on localhost:5500 and your Python API is on localhost:8000, the browser blocks the request by default.
// The Python server must include the right response headers to allow it.
//      Problem	                            What happens	                              Fix
// No CORS headers	                Browser blocks request, console error	            Add CORSMiddleware in FastAPI
// Wrong origin in allow_origins	Request blocked for specific origin	                Use ["*"] in dev, specific domains in production
// Preflight OPTIONS fails	        POST/PUT requests blocked	                        Add allow_methods=["*"]

// Tip: allow_origins=["*"] is fine for development.
// In production, replace "*" with the specific domain of your front end, for example ["https://amerix.co.ke"].
// This ensures only your site can call your API.

// JSON is the universal language

// JavaScript object (lives in memory)
const checkIn = {
  name:     "Aisha Waweru",
  sleep:    7.8,
  water:    10,
  steps:    11400,
  hit_goal: true
};

// Convert to JSON string (what the browser sends over the wire)
const jsonString = JSON.stringify(checkIn);
console.log("Type after stringify:", typeof jsonString);
console.log("JSON string:", jsonString);

// Pretty-print (2-space indent)
console.log("\nPretty JSON:");
console.log(JSON.stringify(checkIn, null, 2));

// Convert back to object (what the browser receives and parses)
const parsed = JSON.parse(jsonString);
console.log("\nType after parse:", typeof parsed);
console.log("Name:", parsed.name);
console.log("Hit goal:", parsed.hit_goal);

// What happens with invalid JSON
try {
  JSON.parse("{bad json}");
} catch (err) {
  console.log("\nParse error caught:", err.message.slice(0, 50));
}

// Arrays serialize and parse correctly too
const log = [{ day: 1, steps: 9800 }, { day: 2, steps: 11200 }];
const logJson = JSON.stringify(log);
const logBack = JSON.parse(logJson);
console.log("\nArray round-trip:", logBack[1].steps);


// Same Pattern Different Context: M-Pesa STK Push Payload.

// JSON is the format for any API, not just health data.
// Here the same JSON.stringify and JSON.parse pattern is applied to an M-Pesa Daraja STK push payload.
// The code is identical. Only the object fields change.

const stkPush = {
  business_shortcode: "174379",
  phone_number: "254712345678",
  amount: 1500,
  account_ref: "JuaKaliOrder",
  description: "Sliding gate deposit",
  timestamp: new Date().toISOString()
};

// Serialize to send to backend
const payload = JSON.stringify(stkPush);
console.log("Serialized payload:");
console.log(payload);

// Pretty-print for readability
console.log("\nFormatted:");
console.log(JSON.stringify(stkPush, null, 2));

// Parse what the backend sends back
const response = JSON.parse('{"MerchantRequestID":"abc-123","ResponseCode":"0","CustomerMessage":"Success. Request accepted for processing"}');
console.log("\nBackend response:");
console.log("Code:", response.ResponseCode);
console.log("Message:", response.CustomerMessage);
