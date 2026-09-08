// SMP Daily AI Coach browser tool.
// This script expects a form with coachForm, inSleep, inWater, and inSteps IDs,
// plus an output element with the coachDisplay ID.

// Step 1: Prediction engine.
// Converts sleep, water, and steps into weighted points, then compares the
// total with the goal threshold and returns the outcome, confidence, and score.
const predictGoal = (sleep, water, steps) => {
  const sleepScore = Math.min(sleep / 8.0, 1.0) * 35;
  const waterScore = Math.min(water / 10.0, 1.0) * 25;
  const stepsScore = Math.min(steps / 12000, 1.0) * 40;
  const totalScore = sleepScore + waterScore + stepsScore;
  const hitGoal = totalScore >= 60;
  const distance = Math.abs(totalScore - 60);
  const confidence = Math.min(0.50 + distance * 0.012, 0.95);

  return { hitGoal, confidence, score: Math.round(totalScore) };
};

// Step 2: Coaching generator.
// Maps the prediction and the sleep and water thresholds to a short,
// actionable coaching message.
const COACHING = {
  "111": ["Strong inputs, strong output. Baseline is locked in.", "Keep this pattern consistent."],
  "110": ["Hit the goal despite low water. Sleep is the primary driver.", "Close the hydration gap tomorrow."],
  "101": ["Water carried today despite low sleep.", "Fix sleep tonight. Low sleep has hidden costs."],
  "100": ["Goal hit through willpower, not system. Willpower runs out.", "Fix the foundation: sleep first, water second."],
  "011": ["Inputs were solid but the goal was missed.", "Audit your schedule. Do not cut sleep or water."],
  "010": ["Sleep is solid but hydration is low, and the goal was missed.", "Add two glasses of water tomorrow."],
  "001": ["Low sleep is the lead variable. Water is fine.", "Get to bed 45 minutes earlier tonight."],
  "000": ["Both inputs are below threshold and the goal was missed.", "Reset tonight: 8 hours sleep minimum, 10 glasses water."],
};

const getCoaching = (sleep, water, hitGoal) => {
  const key = `${hitGoal ? 1 : 0}${sleep >= 7 ? 1 : 0}${water >= 8 ? 1 : 0}`;
  return COACHING[key].join(" ");
};

// Step 3: Form and display.
// Reads the client's one-time check-in, runs both functions, and updates the
// result panel without reloading the page.
const form = document.querySelector('#coachForm');
const display = document.querySelector('#coachDisplay');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const sleep = parseFloat(document.querySelector('#inSleep').value);
  const water = parseInt(document.querySelector('#inWater').value, 10);
  const steps = parseInt(document.querySelector('#inSteps').value, 10);

  if (Number.isNaN(sleep) || Number.isNaN(water) || Number.isNaN(steps)) {
    display.className = 'ai-response idle';
    display.innerHTML = '<div class="label-sm">Error</div><div class="coaching">All three fields are required.</div>';
    return;
  }

  const result = predictGoal(sleep, water, steps);
  const coaching = getCoaching(sleep, water, result.hitGoal);
  const outcome = result.hitGoal ? "HIT GOAL" : "MISS GOAL";
  const confidencePercent = (result.confidence * 100).toFixed(0);

  display.className = `ai-response ${result.hitGoal ? "hit" : "miss"}`;
  display.innerHTML = `
    <div class="label-sm">Prediction</div>
    <div class="prediction">${outcome} (${confidencePercent}% confidence - score: ${result.score}/100)</div>
    <div class="label-sm" style="margin-top:0.8rem;">Coaching</div>
    <div class="coaching">${coaching}</div>
  `;

  const entry = logEntry(sleep, water, steps, result.hitGoal, result.confidence, result.score);
  renderHistory();

  console.log(`Submitted: sleep=${sleep}h water=${water}gl steps=${steps.toLocaleString()}`);
  console.log(`Entry #${entry.id} logged: ${outcome} | ${confidencePercent}% confidence | score ${result.score}`);
});

console.log("Form wired. Use the SMP Coach tool below.");

// Step 4: Session history.
// Keeps each submitted result in memory and renders the time, inputs, outcome,
// score, and confidence in the history table until the page is refreshed.
const sessionLog = [];

const logEntry = (sleep, water, steps, hitGoal, confidence, score) => {
  const entry = {
    id: sessionLog.length + 1,
    time: new Date().toLocaleTimeString(),
    sleep,
    water,
    steps,
    hitGoal,
    confidence,
    score,
  };

  sessionLog.push(entry);
  return entry;
};

const renderHistory = () => {
  const tableEl = document.querySelector('#historyTable');
  if (!sessionLog.length) {
    tableEl.innerHTML = '<tr><td colspan="7" class="empty-history">No entries yet.</td></tr>';
    return;
  }

  tableEl.innerHTML = sessionLog.map((entry) => `
    <tr>
      <td>${entry.id}</td>
      <td>${entry.time}</td>
      <td>${entry.sleep}h</td>
      <td>${entry.water} gl</td>
      <td>${entry.steps.toLocaleString()}</td>
      <td class="${entry.hitGoal ? 'history-hit' : 'history-miss'}">${entry.hitGoal ? 'HIT' : 'MISS'}</td>
      <td>${(entry.confidence * 100).toFixed(0)}%</td>
    </tr>
  `).join('');
};

renderHistory();
console.log("History logging wired. Submit entries using the check-in form.");