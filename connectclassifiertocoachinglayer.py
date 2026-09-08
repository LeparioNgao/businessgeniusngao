import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# --- Training data ---
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
    (True, False, True): ("Water carried today's performance despite low sleep.",
                          "Fix sleep tonight. Hitting goals on low sleep has hidden costs."),
    (True, False, False): ("Goal hit through willpower, not system. That is not repeatable.",
                           "Build the foundation: sleep first, water second."),
    (False, True, True): ("Inputs were solid. The miss came from schedule pressure or load.",
                          "Audit what absorbed the energy. Do not cut sleep or water."),
    (False, True, False): ("Sleep is solid but hydration is low, and the goal was missed.",
                           "Add two glasses of water tomorrow. Hydration shifts step counts directly."),
    (False, False, True): ("Low sleep is the primary variable. Water is fine.",
                           "Get to bed 45 minutes earlier. The compound effect shows within 72 hours."),
    (False, False, False): ("Both inputs are below threshold. A reset is required.",
                            "8 hours sleep minimum. 10 glasses water tomorrow. No shortcuts."),
}

def get_coaching_message(sleep, water, hit_goal):
    key = (bool(hit_goal), sleep >= 7.0, water >= 8)
    line1, line2 = COACHING_TEMPLATES[key]
    return f"{line1} {line2}"

def analyze_day(sleep_hr, water_glasses, bench_kg, day_label=None):
    """Run the full pipeline: predict, score, coach."""
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

# Test on three new days
new_days = [
    (8.0, 10, 92),   # strong day
    (5.5,  4, 70),   # weak day
    (7.2,  7, 84),   # borderline day
    (7.0, 8, 86),
]

for sleep, water, bench in new_days:
    result = analyze_day(sleep, water, bench)
    outcome = "HIT GOAL" if result["hit_goal"] else "MISS GOAL"
    print(f"Prediction: {outcome} ({result['confidence']:.0%} confidence)")
    print(f"Inputs:     sleep={result['sleep_hr']}h, water={result['water_glasses']} glasses, bench={result['bench_kg']}kg")
    print(f"Coach:      {result['coaching']}")
    print()
