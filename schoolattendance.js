// School attendance tracker for a fixed roll of 60 children.
// The page loads this file with schoolattendance.html.

// Step 1: Attendance prediction engine.
// Attendance rate carries most of the score, while on-time attendance adds a
// smaller operational signal. A day is on target at 95% or above.
const TOTAL_CHILDREN = 60;
const ATTENDANCE_TARGET = 0.95;

const predictAttendance = (present, late) => {
  const attendanceRate = present / TOTAL_CHILDREN;
  const onTimeRate = present === 0 ? 0 : (present - late) / present;
  const score = Math.round((attendanceRate * 80) + (onTimeRate * 20));
  const onTarget = attendanceRate >= ATTENDANCE_TARGET;
  const distance = Math.abs(attendanceRate - ATTENDANCE_TARGET);
  const confidence = Math.min(0.50 + distance * 4, 0.95);

  return {
    onTarget,
    attendanceRate,
    onTimeRate,
    confidence,
    score,
  };
};

// Step 2: Attendance coaching generator.
// Chooses a useful follow-up based on attendance, lateness, and absence level.
const getAttendanceCoaching = (present, late, absent, onTarget) => {
  if (onTarget && late === 0) {
    return "Excellent attendance and punctuality. Keep the morning routine consistent.";
  }
  if (onTarget) {
    return "Attendance is on target. Review the late arrivals and follow up with families where needed.";
  }
  if (absent >= 6) {
    return "Attendance is below target today. Contact families and check whether transport, illness, or safeguarding needs are affecting attendance.";
  }
  if (late >= 4) {
    return "Attendance is close to target, but lateness is affecting the day. Review arrival routines with the affected families.";
  }
  return "Attendance is below target. Record the reasons for absence and agree follow-up actions before the next register.";
};

const form = document.querySelector('#attendanceForm');
const resultPanel = document.querySelector('#attendanceResult');
const historyTable = document.querySelector('#attendanceHistory');

// Step 3: Form and display.
// Reads one daily register, validates the counts, and updates the result panel
// without reloading the page.
form.addEventListener('submit', (event) => {
  event.preventDefault();

  const date = document.querySelector('#attendanceDate').value;
  const className = document.querySelector('#className').value.trim();
  const teacher = document.querySelector('#teacherName').value.trim();
  const present = parseInt(document.querySelector('#presentCount').value, 10);
  const late = parseInt(document.querySelector('#lateCount').value, 10);
  const excusedAbsent = parseInt(document.querySelector('#excusedAbsent').value, 10);
  const notes = document.querySelector('#attendanceNotes').value.trim();
  const absent = TOTAL_CHILDREN - present;
  const unexcusedAbsent = absent - excusedAbsent;

  if (!date || !className || !teacher || Number.isNaN(present) || Number.isNaN(late) || Number.isNaN(excusedAbsent)) {
    showError("Complete the date, class, teacher, and attendance counts.");
    return;
  }

  if (present < 0 || present > TOTAL_CHILDREN) {
    showError(`Present must be between 0 and ${TOTAL_CHILDREN}.`);
    return;
  }

  if (late < 0 || late > present) {
    showError("Late arrivals cannot be greater than the number present.");
    return;
  }

  if (excusedAbsent < 0 || excusedAbsent > absent) {
    showError("Excused absence cannot be greater than total absence.");
    return;
  }

  const result = predictAttendance(present, late);
  const outcome = result.onTarget ? "ON TARGET" : "FOLLOW-UP NEEDED";
  const ratePercent = (result.attendanceRate * 100).toFixed(1);
  const coaching = getAttendanceCoaching(present, late, absent, result.onTarget);

  resultPanel.className = `result-panel ${result.onTarget ? "on-target" : "needs-follow-up"}`;
  resultPanel.innerHTML = `
    <div class="result-kicker">${outcome}</div>
    <div class="result-rate">${ratePercent}% attendance</div>
    <div class="result-summary">${present} present, ${absent} absent, ${late} late</div>
    <div class="result-coaching">${coaching}</div>
    <div class="result-meta">Confidence ${(result.confidence * 100).toFixed(0)}% · score ${result.score}/100</div>
  `;

  logAttendance({
    date,
    className,
    teacher,
    present,
    absent,
    late,
    excusedAbsent,
    unexcusedAbsent,
    notes,
    attendanceRate: result.attendanceRate,
    onTarget: result.onTarget,
    confidence: result.confidence,
    score: result.score,
  });

  form.reset();
  document.querySelector('#attendanceDate').value = date;
});

const showError = (message) => {
  resultPanel.className = "result-panel error";
  resultPanel.innerHTML = `<div class="result-kicker">CHECK REGISTER</div><div class="result-coaching">${message}</div>`;
};

// Step 4: Session history.
// Keeps daily registers in memory until refresh and displays the information a
// school office needs for review and follow-up.
const attendanceLog = [];

const logAttendance = (entry) => {
  attendanceLog.push({
    id: attendanceLog.length + 1,
    loggedAt: new Date().toLocaleTimeString(),
    ...entry,
  });
  renderAttendanceHistory();
};

const renderAttendanceHistory = () => {
  if (!attendanceLog.length) {
    historyTable.innerHTML = '<tr><td colspan="14" class="empty-history">No registers logged yet.</td></tr>';
    return;
  }

  historyTable.innerHTML = attendanceLog.map((entry) => `
    <tr>
      <td>${entry.date}</td>
      <td>${entry.className}</td>
      <td>${entry.present}</td>
      <td>${entry.absent}</td>
      <td>${entry.late}</td>
      <td>${entry.excusedAbsent}</td>
      <td>${entry.unexcusedAbsent}</td>
      <td>${(entry.attendanceRate * 100).toFixed(1)}%</td>
      <td class="${entry.onTarget ? 'status-good' : 'status-action'}">${entry.onTarget ? 'ON TARGET' : 'FOLLOW-UP'}</td>
      <td>${entry.score}/100</td>
      <td>${(entry.confidence * 100).toFixed(0)}%</td>
      <td>${entry.teacher}</td>
      <td>${entry.loggedAt}</td>
      <td>${entry.notes || '—'}</td>
    </tr>
  `).join('');
};

renderAttendanceHistory();
