import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Training data: [feed_kg_per_day, lactation_day]
# Label: 1 = above 15L that day, 0 = below
X = np.array([
    [6.5, 30],[7.0, 45],[5.5, 20],[7.5, 60],[6.0, 25],
    [8.0, 75],[5.0, 15],[7.2, 50],[6.8, 40],[7.8, 70],
    [5.8, 22],[7.3, 55],[6.2, 28],[8.1, 80],[5.3, 18],
    [7.1, 48],[6.6, 35],[7.6, 65],[5.7, 21],[7.9, 72],
])
y = np.array([1,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1])

clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X, y)

def predict_cow_yield(feed_kg, lactation_day):
    inputs = np.array([[feed_kg, lactation_day]])
    pred = clf.predict(inputs)[0]
    proba = clf.predict_proba(inputs)[0]
    confidence = max(proba) * 100
    status = "Above 15L target" if pred == 1 else "Below target"
    return status, round(confidence, 1)

cows = [
    ("Cow 1 (Kamau farm)", 7.2, 50),
    ("Cow 2 (Wanjiku farm)", 5.5, 20),
    ("Cow 3 (Mwangi farm)", 7.8, 70),
]
print("Githunguri Dairy: Daily Yield Predictions")
print()
for name, feed, day in cows:
    status, conf = predict_cow_yield(feed, day)
    print(f"  {name}")
    print(f"    Feed={feed}kg  Lactation day={day}")
    print(f"    => {status} ({conf:.0f}% confidence)")
    print()