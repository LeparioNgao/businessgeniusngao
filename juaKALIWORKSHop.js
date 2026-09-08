// This object stores the workshop information.
const workshop = {
  name: "Kamau Metalworks",
  town: "Gikomba, Nairobi",
  craftsman: "Joseph Kamau"
};

// This array stores all the jobs done by the workshop.
const jobs = [
  { type: "Sliding gate",  materials_kes: 18000, labour_kes: 8000, paid: true  },
  { type: "Window grills", materials_kes:  6500, labour_kes: 4500, paid: true  },
  { type: "Door frame",    materials_kes:  4200, labour_kes: 2800, paid: false },
  { type: "Roof sheet",    materials_kes:  9800, labour_kes: 3200, paid: true  },
  { type: "Security door", materials_kes: 12000, labour_kes: 7000, paid: false },
];

// This calculates the money that has already been paid for.
const totalRevenue = jobs
  .filter(j => j.paid)
  .reduce((sum, j) => sum + j.materials_kes + j.labour_kes, 0);

// This counts how many jobs are still unpaid.
const unpaidCount = jobs.filter(j => !j.paid).length;

// Show basic workshop details in the console.
console.log(`Workshop: ${workshop.name} | ${workshop.town}`);
console.log(`Craftsman: ${workshop.craftsman}`);
console.log(`Jobs completed: ${jobs.length}`);
console.log(`Revenue collected: KES ${totalRevenue.toLocaleString()}`);
console.log(`Unpaid jobs: ${unpaidCount}`);
console.log("\nJob breakdown:");

// Loop through each job and print its total cost and payment status.
for (const job of jobs) {
  const total = job.materials_kes + job.labour_kes;
  const status = job.paid ? "PAID" : "UNPAID";
  console.log(`  ${job.type} | KES ${total.toLocaleString()} | ${status}`);
}

// This object stores the weekly health and fitness data.
const workout = {
  name1: "Lepario Leuyan",
  steps: [7500, 8200, 10500, 15000, 6500, 8500, 12400],
  sleep: [8.0, 7.0, 6.5, 8.0, 7.5, 8.0, 8.5],
  water: [2.5, 2.0, 1.8, 2.6, 1.9, 2.2, 2.8],
  benchPress: [20, 15, 25, 22, 18, 24, 30],
};

// This function grades the weekly progress based on the fitness goals.
function gradeWeeklyProgress(user) {
  // Set the minimum target for each habit.
  const minDailySteps = 10000;
  const minSleepHours = 8;
  const minWaterLiters = 2;
  const minBenchReps = 20;

  // Check each day against the goals and store the result.
  const weeklyProgress = user.steps.map((steps, index) => {
    const sleep = user.sleep[index];
    const water = user.water[index];
    const benchPress = user.benchPress[index];

    const stepsGoalMet = steps >= minDailySteps;
    const sleepGoalMet = sleep >= minSleepHours;
    const waterGoalMet = water >= minWaterLiters;
    const benchGoalMet = benchPress >= minBenchReps;
    const onTrack = stepsGoalMet && sleepGoalMet && waterGoalMet && benchGoalMet;

    return {
      day: index + 1,
      name1: user.name1,
      steps,
      sleep,
      water,
      benchPress,
      stepsGoalMet,
      sleepGoalMet,
      waterGoalMet,
      benchGoalMet,
      onTrack,
    };
  });

  // Find how many days were fully on track.
  const daysOnTrack = weeklyProgress.filter(day => day.onTrack).length;

  // Calculate the weekly averages.
  const averageSteps = Math.round(
    user.steps.reduce((sum, steps) => sum + steps, 0) / user.steps.length
  );
  const averageSleep = (
    user.sleep.reduce((sum, hours) => sum + hours, 0) / user.sleep.length
  ).toFixed(1);
  const averageWater = (
    user.water.reduce((sum, liters) => sum + liters, 0) / user.water.length
  ).toFixed(1);
  const averageBenchPress = Math.round(
    user.benchPress.reduce((sum, reps) => sum + reps, 0) / user.benchPress.length
  );

  // Give a simple weekly label based on progress.
  let weeklyGrade = "Needs attention";
  if (
    daysOnTrack >= 5 &&
    averageSteps >= minDailySteps &&
    Number(averageSleep) >= minSleepHours &&
    Number(averageWater) >= minWaterLiters &&
    averageBenchPress >= minBenchReps
  ) {
    weeklyGrade = "Excellent";
  } else if (daysOnTrack >= 3) {
    weeklyGrade = "Good";
  } else if (daysOnTrack >= 1) {
    weeklyGrade = "Fair";
  }

  return {
    name1: user.name1,
    minDailySteps,
    minSleepHours,
    minWaterLiters,
    minBenchReps,
    weeklyProgress,
    daysOnTrack,
    averageSteps,
    averageSleep,
    averageWater,
    averageBenchPress,
    weeklyGrade,
  };
}

// Run the function and store the result.
const report = gradeWeeklyProgress(workout);

// Print the weekly summary.
console.log(`\nWeekly progress for ${report.name1}`);
console.log(
  `Target: ${report.minDailySteps.toLocaleString()} steps/day, ${report.minSleepHours}h sleep, ${report.minWaterLiters}L water, ${report.minBenchReps} reps bench press`
);

// Show each day with its habits and whether it was on track.
for (const day of report.weeklyProgress) {
  const stepStatus = day.stepsGoalMet ? "Steps OK" : "Low steps";
  const sleepStatus = day.sleepGoalMet ? "Sleep OK" : "Low sleep";
  const waterStatus = day.waterGoalMet ? "Water OK" : "Low water";
  const benchStatus = day.benchGoalMet ? "Bench OK" : "Low bench";

  console.log(
    `Day ${day.day}: ${day.steps.toLocaleString()} steps | ${day.sleep}h sleep | ${day.water}L water | ${day.benchPress} reps | ${stepStatus} | ${sleepStatus} | ${waterStatus} | ${benchStatus} | ${day.onTrack ? "ON TRACK" : "OFF TRACK"}`
  );
}

console.log(
  `Average steps: ${report.averageSteps.toLocaleString()} | Average sleep: ${report.averageSleep}h | Average water: ${report.averageWater}L | Average bench press: ${report.averageBenchPress} reps`
);
console.log(`Weekly grade: ${report.weeklyGrade}`);