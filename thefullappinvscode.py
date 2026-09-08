#Moving from browser simulation to production requires two changes:
# loading data from a CSV file and replacing the template coaching with a live OpenAI API call.
# The rest of the architecture stays identical.

import pandas as pd
import numpy as np
import openai, os, joblib
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if __file__ else os.getcwd()
DATA_PATH = os.path.join(BASE_DIR, "smp_log.csv")
MODEL_PATH = os.path.join(BASE_DIR, "smp_coach_model.pkl")
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key) if api_key else None


def ensure_training_data():
    if not os.path.exists(DATA_PATH):
        sample_rows = [
            [6.5, 6, 80, 8500], [7.2, 8, 85, 12000], [5.8, 5, 75, 9000], [8.0, 10, 90, 13800],
            [7.5, 9, 88, 12800], [6.0, 6, 78, 8600], [7.8, 8, 86, 12500], [8.2, 10, 92, 14200],
            [5.5, 4, 70, 7800], [7.0, 7, 82, 11400], [6.8, 8, 84, 11800], [8.5, 11, 95, 14900],
            [7.3, 9, 89, 12900], [6.2, 6, 76, 9200], [7.9, 10, 91, 13600], [5.9, 5, 73, 8200],
            [8.1, 11, 93, 14500], [7.4, 8, 87, 12700], [6.7, 7, 83, 10600], [8.3, 10, 94, 14700],
            [5.6, 4, 71, 7900], [7.1, 8, 85, 11600], [8.0, 9, 90, 13300], [6.4, 6, 77, 8800],
            [7.6, 9, 88, 13000], [8.4, 11, 96, 15000], [6.3, 7, 79, 9800], [7.7, 10, 91, 13900],
            [6.9, 7, 81, 11000], [8.2, 9, 93, 14100], [5.7, 5, 72, 8100], [7.8, 9, 89, 13100],
        ]
        df = pd.DataFrame(sample_rows, columns=["sleep_hr", "water_glasses", "bench_kg", "steps"])
        df.to_csv(DATA_PATH, index=False)


# Create the CSV if it is missing and then load it
ensure_training_data()
df = pd.read_csv(DATA_PATH)

if os.path.exists(MODEL_PATH):
    clf = joblib.load(MODEL_PATH)
else:
    X = df[["sleep_hr", "water_glasses", "bench_kg"]].to_numpy()
    y = (df["steps"] >= 10000).astype(int).to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Save trained model so you do not retrain every time
    joblib.dump(clf, MODEL_PATH)

def get_coaching_message(sleep, water, bench, hit_goal, confidence):
    if client is None:
        status = "HIT GOAL" if hit_goal else "MISS GOAL"
        if hit_goal:
            return (f"Strong day. You hit the target with {confidence:.0%} confidence. "
                    "Keep the same recovery rhythm and protect the habits that got you there.")
        return (f"The model projects a miss at {confidence:.0%} confidence. "
                "Add one more hour of sleep and two more glasses of water to raise your output next session.")

    prompt = (f"Athlete logged: sleep {sleep}h, water {water} glasses, bench {bench}kg. "
              f"Model predicts: {'HIT GOAL' if hit_goal else 'MISS GOAL'} at {confidence:.0%} confidence. "
              "Give a direct 2-sentence coaching response. No filler. No hedging.")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                 "content": "You are an SMP performance coach. Data-driven. Direct. Two sentences maximum."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception:
        status = "HIT GOAL" if hit_goal else "MISS GOAL"
        if hit_goal:
            return (f"Strong day. You hit the target with {confidence:.0%} confidence. "
                    "Keep the same recovery rhythm and protect the habits that got you there.")
        return (f"The model projects a miss at {confidence:.0%} confidence. "
                "Add one more hour of sleep and two more glasses of water to raise your output next session.")

def analyze_day(sleep_hr, water_glasses, bench_kg, day_label=None):
    features = np.array([[sleep_hr, water_glasses, bench_kg]])
    prediction = clf.predict(features)[0]
    confidence = clf.predict_proba(features)[0][prediction]
    coaching = get_coaching_message(sleep_hr, water_glasses, bench_kg, prediction, confidence)
    return {
        "label":      day_label or "Day",
        "hit_goal":  bool(prediction),
        "confidence": confidence,
        "coaching":   coaching,
    }


if __name__ == "__main__":
    sample_days = [
        (8.0, 10, 90, "Day 1"),
        (6.5, 6, 80, "Day 2"),
        (7.5, 8, 88, "Day 3"),
    ]

    for sleep, water, bench, label in sample_days:
        result = analyze_day(sleep, water, bench, label)
        outcome = "HIT GOAL" if result["hit_goal"] else "MISS GOAL"
        print(f"{result['label']}: {outcome} ({result['confidence']:.0%} confidence)")
        print(result["coaching"])
        print("-" * 60)