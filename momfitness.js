const STORAGE_KEY = "momentum-bulk-records";
const BULK_TARGETS = {
  calories: 2900,
  protein: 150,
  steps: 8000,
  water: 2.5,
  sleep: 8,
  workout: 45,
};

const form = document.querySelector("#fitnessForm");
const resultPanel = document.querySelector("#resultPanel");
const historyTable = document.querySelector("#historyTable");
const forecastValue = document.querySelector("#forecastValue");
const forecastCopy = document.querySelector("#forecastCopy");
const forecastCard = document.querySelector("#forecastCard");
const records = loadRecords();

const today = new Date().toISOString().slice(0, 10);
document.querySelector("#fitnessDate").value = today;

function getStoredRecords() {
  try {
    return localStorage.getItem(STORAGE_KEY) || "[]";
  } catch (error) {
    return "[]";
  }
}

function loadRecords() {
  try {
    const saved = JSON.parse(getStoredRecords());
    return Array.isArray(saved) ? saved : [];
  } catch (error) {
    return [];
  }
}

function saveRecords() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(records));
    return true;
  } catch (error) {
    return false;
  }
}

function average(field) {
  if (!records.length) return BULK_TARGETS[field];
  return records.reduce((total, record) => total + record[field], 0) / records.length;
}

function calculateVerdict(entry) {
  const checks = [
    Math.min(entry.calories / BULK_TARGETS.calories, 1.15) / 1.15,
    Math.min(entry.protein / BULK_TARGETS.protein, 1),
    Math.min(entry.steps / BULK_TARGETS.steps, 1),
    Math.min(entry.water / BULK_TARGETS.water, 1),
    Math.min(entry.sleep / BULK_TARGETS.sleep, 1),
    entry.workout >= BULK_TARGETS.workout ? 1 : entry.workout / BULK_TARGETS.workout,
  ];
  const score = Math.round(checks.reduce((total, value) => total + value, 0) / checks.length * 100);
  const surplusSignal = entry.calories >= BULK_TARGETS.calories && entry.protein >= BULK_TARGETS.protein;
  const recoverySignal = entry.sleep >= 7 && entry.water >= 2;
  const onTarget = score >= 78 && surplusSignal && recoverySignal;
  return { score, onTarget, checks };
}

function getCoaching(entry, verdict) {
  if (verdict.onTarget) {
    return "Strong bulk day. You gave growth enough fuel and recovery enough support. Repeat the basics tomorrow.";
  }
  const lowest = [
    { value: entry.calories / BULK_TARGETS.calories, message: "Add a calorie-dense snack or larger serving to protect the surplus." },
    { value: entry.protein / BULK_TARGETS.protein, message: "Protein is the clearest lever today. Add a protein-rich meal before the day ends." },
    { value: entry.sleep / BULK_TARGETS.sleep, message: "Tonight's recovery is the next win: protect a consistent sleep window." },
    { value: entry.water / BULK_TARGETS.water, message: "Keep a bottle nearby and close the hydration gap before bed." },
    { value: entry.workout / BULK_TARGETS.workout, message: "A short, deliberate strength session can keep the training habit alive." },
  ].sort((first, second) => first.value - second.value)[0];
  return `Today is a useful signal, not a failure. ${lowest.message}`;
}

function readEntry() {
  const fields = ["bodyWeight", "calories", "protein", "steps", "water", "sleep", "workout"];
  const entry = { date: document.querySelector("#fitnessDate").value };
  fields.forEach((field) => { entry[field] = Number(document.querySelector(`#${field}`).value); });
  return entry;
}

function showError(message) {
  resultPanel.className = "panel result error";
  resultPanel.innerHTML = `<div class="result-kicker">Check today's entry</div><h2 class="result-title">One more detail.</h2><p class="result-summary">${message}</p>`;
}

form.addEventListener("invalid", () => {
  showError("Complete every field before saving today's check-in.");
}, true);

function renderResult(entry, verdict) {
  const comparison = records.length > 1 ? ` Personal baseline: ${average("calories").toFixed(0)} kcal/day.` : " Baseline created today.";
  resultPanel.className = `panel result ${verdict.onTarget ? "on-target" : "needs-action"}`;
  resultPanel.innerHTML = `
    <div class="result-kicker">${verdict.onTarget ? "On target" : "Adjustment suggested"}</div>
    <h2 class="result-title">${verdict.score}/100 consistency</h2>
    <p class="result-summary">${entry.calories} kcal, ${entry.protein}g protein, ${entry.sleep}h sleep, and ${entry.workout} minutes trained.${comparison}</p>
    <div class="result-coaching">${getCoaching(entry, verdict)}</div>
    <div class="result-meta">Adaptive confidence: ${Math.min(95, 55 + records.length * 5)}% · ${records.length} day${records.length === 1 ? "" : "s"} learning</div>
  `;
}

function renderForecast() {
  if (!records.length) return;
  const consistency = records.reduce((total, record) => total + record.score, 0) / records.length;
  const firstWeight = records[0].bodyWeight;
  const latestWeight = records[records.length - 1].bodyWeight;
  const dailyChange = records.length > 1 ? (latestWeight - firstWeight) / (records.length - 1) : 0;
  const weeklyGain = dailyChange * 7;
  const projectedGain = weeklyGain * 12;
  const direction = projectedGain >= 0.2 ? "+" : "";
  forecastValue.textContent = `${direction}${projectedGain.toFixed(1)} kg`;
  forecastCopy.textContent = `${consistency.toFixed(0)}% average consistency so far. At this trend, your projected 12-week change is ${direction}${projectedGain.toFixed(1)} kg. Keep the forecast honest by logging regularly.`;
  forecastCard.classList.toggle("on-target", consistency >= 78);
}

function renderHistory() {
  document.querySelector("#daysLogged").textContent = records.length;
  const consistency = records.length ? records.reduce((total, record) => total + record.score, 0) / records.length : 0;
  document.querySelector("#consistencyScore").textContent = records.length ? `${consistency.toFixed(0)}%` : "--";
  if (records.length > 1) {
    const change = records[records.length - 1].bodyWeight - records[0].bodyWeight;
    document.querySelector("#weightTrend").textContent = `${change >= 0 ? "+" : ""}${change.toFixed(1)} kg`;
  }
  if (!records.length) {
    historyTable.innerHTML = '<tr><td colspan="10" class="empty-history">No days logged yet.</td></tr>';
    return;
  }
  historyTable.innerHTML = records.slice().reverse().map((entry) => `
    <tr>
      <td>${entry.date}</td><td>${entry.bodyWeight.toFixed(1)} kg</td><td>${entry.calories}</td><td>${entry.protein} g</td>
      <td>${entry.steps.toLocaleString()}</td><td>${entry.water.toFixed(1)} L</td><td>${entry.sleep.toFixed(1)} h</td><td>${entry.workout} min</td>
      <td class="${entry.onTarget ? "status-good" : "status-action"}">${entry.onTarget ? "ON TARGET" : "ADJUST"}</td><td>${entry.score}/100</td>
    </tr>`).join("");
  renderForecast();
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const entry = readEntry();
  if (!entry.date || Object.values(entry).some((value) => typeof value === "number" && (!Number.isFinite(value) || value < 0))) {
    showError("Enter a date and non-negative numbers for every measurement.");
    return;
  }
  const verdict = calculateVerdict(entry);
  Object.assign(entry, verdict);
  const existingIndex = records.findIndex((record) => record.date === entry.date);
  if (existingIndex >= 0) records[existingIndex] = entry;
  else records.push(entry);
  records.sort((first, second) => first.date.localeCompare(second.date));
  if (!saveRecords()) {
    showError("The record was calculated, but this browser could not save it. Try opening the page in Chrome again or allow site storage.");
    return;
  }
  renderResult(entry, verdict);
  renderHistory();
  form.reset();
  document.querySelector("#fitnessDate").value = entry.date;
});

document.querySelector("#clearHistory").addEventListener("click", () => {
  if (!records.length || !window.confirm("Delete all saved fitness records?")) return;
  records.length = 0;
  saveRecords();
  renderHistory();
  forecastValue.textContent = "Waiting";
  forecastCopy.textContent = "Log your first day to create a baseline and see the direction of your bulk.";
});

renderHistory();