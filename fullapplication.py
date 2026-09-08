# Full Application with Batch Output and Summary
# The complete application processes multiple days in a batch, prints a formatted coaching report for each day, then prints an overall summary:
# hit rate, average confidence, and the input difference between hit and miss days.

# Concept: Batch processing
# Running the same function on a list of inputs and collecting all results before printing.
# You do not print inside the processing loop.
# You collect, then report. This is how production applications are structured.

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# --- Training ---
X = np.array([
    [6.5,6,80],[7.2,8,85],[5.8,5,75],[8.0,10,90],[7.5,9,88],
    [6.0,6,78],[7.8,8,86],[8.2,10,92],[5.5,4,70],[7.0,7,82],
    [6.8,8,84],[8.5,11,95],[7.3,9,89],[6.2,6,76],[7.9,10,91],
    [5.9,5,73],[8.1,11,93],[7.4,8,87],[6.7,7,83],[8.3,10,94],
    [5.6,4,71],[7.1,8,85],[8.0,9,90],[6.4,6,77],[7.6,9,88],
    [8.4,11,96],[6.3,7,79],[7.7,10,91]
])
y = np.array([0,1,0,1,1,0,1,1,0,1,1,1,1,0,1,0,1,1,0,1,0,1,1,0,1,1,0,1])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# --- Coaching templates ---
COACHING_TEMPLATES = {
    (True, True, True):  ("Strong inputs, strong output. Baseline is locked in.",
                          "Keep this pattern consistent."),
    (True, True, False): ("Hit the goal despite low water. Sleep is the primary driver.",
                          "Close the hydration gap tomorrow."),
    (True, False, True): ("Water carried today despite low sleep.",
                          "Fix sleep tonight. Low sleep has costs that accumulate."),
    (True, False, False): ("Goal hit through willpower, not system. That is not repeatable.",
                           "Build the foundation: sleep first, water second."),
    (False, True, True): ("Inputs were solid. The miss came from schedule pressure or load.",
                          "Audit what absorbed the energy. Do not cut sleep or water."),
    (False, True, False): ("Sleep is solid but hydration is low, and the goal was missed.",
                           "Add two glasses of water tomorrow. Hydration shifts step counts directly."),
    (False, False, True): ("Low sleep is the primary variable. Water is fine.",
                           "Get to bed 45 minutes earlier. The effect shows within 72 hours."),
    (False, False, False): ("Both inputs are below threshold. A reset is required.",
                            "8 hours sleep minimum. 10 glasses water tomorrow. No shortcuts."),
}

def get_coaching_message(sleep, water, hit_goal):
    key = (bool(hit_goal), sleep >= 7.0, water >= 8)
    line1, line2 = COACHING_TEMPLATES[key]
    return f"{line1} {line2}"

def analyze_day(sleep_hr, water_glasses, bench_kg, day_label=None):
    features = np.array([[sleep_hr, water_glasses, bench_kg]])
    prediction = clf.predict(features)[0]
    proba = clf.predict_proba(features)[0]
    confidence = proba[prediction]
    coaching = get_coaching_message(sleep_hr, water_glasses, prediction)
    return {
        "label":         day_label or "Day",
        "sleep_hr":      sleep_hr,
        "water_glasses": water_glasses,
        "bench_kg":      bench_kg,
        "hit_goal":      bool(prediction),
        "confidence":    confidence,
        "coaching":      coaching,
    }

# --- Batch of incoming days ---
incoming_days = [
    ("Day 29", 8.0, 10, 92),
    ("Day 30", 5.5,  4, 70),
    ("Day 31", 7.2,  7, 84),
    ("Day 32", 8.5, 11, 95),
    ("Day 33", 6.1,  5, 76),
    ("Day 34", 7.8,  9, 88),
    ("Day 35", 5.9,  6, 73),
]

# Process all days, collect before printing
results = [analyze_day(sleep, water, bench, label)
           for label, sleep, water, bench in incoming_days]

# --- Individual reports ---
SEP = "=" * 62
print(SEP)
print("    SMP PERFORMANCE COACH  |  DAILY REPORTS")
print(SEP)

for r in results:
    outcome = "HIT GOAL" if r["hit_goal"] else "MISS GOAL"
    print(f"\n{r['label']}")
    print(f"  Outcome:  {outcome} ({r['confidence']:.0%} confidence)")
    print(f"  Inputs:   sleep={r['sleep_hr']}h  water={r['water_glasses']}gl  bench={r['bench_kg']}kg")
    print(f"  Coach:    {r['coaching']}")

# --- Summary ---
print()
print(SEP)
print("    SUMMARY")
print(SEP)

total  = len(results)
hits   = sum(1 for r in results if r["hit_goal"])
misses = total - hits
avg_conf = np.mean([r["confidence"] for r in results])

hit_days  = [r for r in results if r["hit_goal"]]
miss_days = [r for r in results if not r["hit_goal"]]

avg_sleep_hit  = np.mean([r["sleep_hr"]      for r in hit_days])  if hit_days  else 0
avg_water_hit  = np.mean([r["water_glasses"]  for r in hit_days])  if hit_days  else 0
avg_sleep_miss = np.mean([r["sleep_hr"]      for r in miss_days]) if miss_days else 0
avg_water_miss = np.mean([r["water_glasses"]  for r in miss_days]) if miss_days else 0

print(f"\n  Days analyzed:    {total}")
print(f"  Goals hit:        {hits} / {total}  ({hits/total:.0%})")
print(f"  Goals missed:     {misses} / {total}  ({misses/total:.0%})")
print(f"  Avg confidence:   {avg_conf:.0%}")
print()
print("  On HIT days:")
print(f"    avg sleep:  {avg_sleep_hit:.1f}h  |  avg water: {avg_water_hit:.1f} glasses")
print()
print("  On MISS days:")
print(f"    avg sleep:  {avg_sleep_miss:.1f}h  |  avg water: {avg_water_miss:.1f} glasses")
print()
sleep_diff = avg_sleep_hit - avg_sleep_miss
water_diff = avg_water_hit - avg_water_miss
print(f"  HIT days averaged {sleep_diff:+.1f}h more sleep and {water_diff:+.1f} more glasses of water")
print()
print(SEP)
print("    End of report")
print(SEP)
