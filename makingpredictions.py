#Training a model is the setup. Prediction is the product.
# Once a model is trained, you send it new inputs and it returns answers.
# This lesson covers how to predict for single inputs and batches, how to save a trained model to disk so you do not retrain every time, and how to load it back for future use.

#Learning Objectives
# 1. Predict a single new data point with .predict()
# 2. Get probability scores with .predict_proba()
# 3. Save a trained model to a file using joblib
# 4. Load a saved model and use it without retraining
# 5. Build a simple prediction function

# 1. Single and Batch Predictions

#.predict(X) takes a 2D array of inputs and returns predictions.
# Each row is one set of inputs.
# For a single prediction you still wrap it in a 2D array: np.array([[sleep, water, bench]]).
# The output is an array of predictions, one per row.

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X = np.array([[7.5,7,80],[8.0,8,82],[6.5,6,78],[7.0,9,85],[9.0,8,80],[7.5,7,83],[8.0,8,84],[6.0,6,81],[8.5,9,85],[7.0,8,80],[7.5,8,86],[9.0,7,79],[7.0,9,84],[7.5,8,83],[7.0,7,82],[8.0,8,86],[6.5,6,79],[7.5,9,88],[8.0,8,81],[7.0,7,85],[8.5,9,87],[7.0,8,82],[7.5,8,86],[6.5,6,80],[8.0,9,87],[9.5,7,79],[7.0,8,84],[8.0,9,86]])
steps = np.array([9200,10500,8800,11000,7600,9400,10200,8900,10800,9100,11200,7900,10000,9700,9500,10300,8600,11500,8200,9800,10600,9000,10100,8400,10900,7500,9600,10400])
y = (steps >= 10000).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
clf = RandomForestClassifier(n_estimators=20, random_state=42)
clf.fit(X_train, y_train)

# Single prediction (must still be 2D)
single_day = np.array([[8.0, 8, 84]])  # 8hr sleep, 8 water, 84kg bench
pred = clf.predict(single_day)[0]
label = "Goal hit" if pred == 1 else "Below goal"
print(f"Single prediction: {label}")

# Batch predictions
new_days = np.array([
    [8.0, 8, 84],   # good sleep, good hydration
    [6.0, 5, 78],   # poor sleep, low water
    [9.0, 9, 87],   # excellent sleep and hydration
    [7.0, 7, 82],   # average day
    [6.5, 6, 79],   # rough day
])

preds = clf.predict(new_days)
print("\nBatch predictions:")
for inputs, pred in zip(new_days, preds):
    label = "Goal hit" if pred == 1 else "Below goal"
    print(f"  sleep={inputs[0]}h water={int(inputs[1])} bench={int(inputs[2])}kg => {label}")

# 2. Prediction Probabilities.

#.predict_proba() returns the confidence of the prediction, not just the label.
# Each row has two values: probability of class 0 and probability of class 1.
# This lets you set your own threshold or communicate uncertainty.

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X = np.array([[7.5,7,80],[8.0,8,82],[6.5,6,78],[7.0,9,85],[9.0,8,80],[7.5,7,83],[8.0,8,84],[6.0,6,81],[8.5,9,85],[7.0,8,80],[7.5,8,86],[9.0,7,79],[7.0,9,84],[7.5,8,83],[7.0,7,82],[8.0,8,86],[6.5,6,79],[7.5,9,88],[8.0,8,81],[7.0,7,85],[8.5,9,87],[7.0,8,82],[7.5,8,86],[6.5,6,80],[8.0,9,87],[9.5,7,79],[7.0,8,84],[8.0,9,86]])
steps = np.array([9200,10500,8800,11000,7600,9400,10200,8900,10800,9100,11200,7900,10000,9700,9500,10300,8600,11500,8200,9800,10600,9000,10100,8400,10900,7500,9600,10400])
y = (steps >= 10000).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
clf = RandomForestClassifier(n_estimators=20, random_state=42)
clf.fit(X_train, y_train)

new_days = np.array([[8.0,8,84],[6.0,5,78],[9.0,9,87],[7.0,7,82]])
probas = clf.predict_proba(new_days)

print("Prediction with confidence:")
for inputs, proba in zip(new_days, probas):
    prob_hit = proba[1]  # probability of class 1 (hit goal)
    label = "Goal hit" if prob_hit >= 0.5 else "Below goal"
    confidence = max(proba) * 100
    print(f"  sleep={inputs[0]}h water={int(inputs[1])} bench={int(inputs[2])}kg")
    print(f"    => {label}  (confidence: {confidence:.0f}%)")

# 3. Saving and Loading a Model.

#Retraining every time is wasteful.
# Save the trained model to a file with joblib.dump().
# Load it back later with joblib.load(). The loaded model works identically to the trained one.

# In VS Code: save the model
import joblib
from sklearn.ensemble import RandomForestClassifier

# (after training clf)
joblib.dump(clf, "step_goal_model.joblib")
print("Model saved.")

# In VS Code: load and use
import joblib
import numpy as np

clf = joblib.load("step_goal_model.joblib")

# Predict without retraining
new_day = np.array([[8.0, 8, 84]])
pred = clf.predict(new_day)[0]
print("Prediction:", "Goal hit" if pred == 1 else "Below goal")


#In your VS Code projects, use joblib instead of pickle for scikit-learn models.
# It is faster for large arrays and is the officially recommended serialization method for scikit-learn.
import numpy as np
import io, joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X = np.array([[7.5,7,80],[8.0,8,82],[6.5,6,78],[7.0,9,85],[9.0,8,80],[7.5,7,83],[8.0,8,84],[6.0,6,81],[8.5,9,85],[7.0,8,80],[7.5,8,86],[9.0,7,79],[7.0,9,84],[7.5,8,83],[7.0,7,82],[8.0,8,86],[6.5,6,79],[7.5,9,88],[8.0,8,81],[7.0,7,85],[8.5,9,87],[7.0,8,82],[7.5,8,86],[6.5,6,80],[8.0,9,87],[9.5,7,79],[7.0,8,84],[8.0,9,86]])
steps = np.array([9200,10500,8800,11000,7600,9400,10200,8900,10800,9100,11200,7900,10000,9700,9500,10300,8600,11500,8200,9800,10600,9000,10100,8400,10900,7500,9600,10400])
y = (steps >= 10000).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
clf = RandomForestClassifier(n_estimators=20, random_state=42)
clf.fit(X_train, y_train)

# Simulate save (to bytes in memory)
buffer = io.BytesIO()
joblib.dump(clf, buffer)
print("Model serialized (saved to memory buffer)")

# Simulate load
buffer.seek(0)
loaded_clf = joblib.load(buffer)
print("Model loaded from buffer")

# Predict with the loaded model
new_days = np.array([[8.0, 8, 84], [6.0, 5, 78], [9.0, 9, 87]])
preds = loaded_clf.predict(new_days)
print("\nLoaded model predictions:")
for inputs, pred in zip(new_days, preds):
    label = "Goal hit" if pred == 1 else "Below goal"
    print(f"  {inputs} => {label}")

# 4. A Reusable Prediction Function.

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Train
X = np.array([[7.5,7,80],[8.0,8,82],[6.5,6,78],[7.0,9,85],[9.0,8,80],[7.5,7,83],[8.0,8,84],[6.0,6,81],[8.5,9,85],[7.0,8,80],[7.5,8,86],[9.0,7,79],[7.0,9,84],[7.5,8,83],[7.0,7,82],[8.0,8,86],[6.5,6,79],[7.5,9,88],[8.0,8,81],[7.0,7,85],[8.5,9,87],[7.0,8,82],[7.5,8,86],[6.5,6,80],[8.0,9,87],[9.5,7,79],[7.0,8,84],[8.0,9,86]])
steps_y = np.array([9200,10500,8800,11000,7600,9400,10200,8900,10800,9100,11200,7900,10000,9700,9500,10300,8600,11500,8200,9800,10600,9000,10100,8400,10900,7500,9600,10400])
y = (steps_y >= 10000).astype(int)
clf = RandomForestClassifier(n_estimators=20, random_state=42)
clf.fit(X, y)

# Reusable function
def predict_day(sleep_hours, water_glasses, bench_kg):
    """
    Predict whether today will be a 10k step day.
    Returns: dict with prediction, confidence, and recommendation.
    """
    inputs = np.array([[sleep_hours, water_glasses, bench_kg]])
    pred = clf.predict(inputs)[0]
    proba = clf.predict_proba(inputs)[0]
    confidence = max(proba)

    result = {
        "hit_goal": bool(pred),
        "confidence": round(confidence * 100, 1),
        "recommendation": ""
    }

    if pred == 0 and confidence > 0.7:
        result["recommendation"] = "Low step day likely. Schedule a walk this afternoon."
    elif pred == 1 and confidence > 0.7:
        result["recommendation"] = "High step day likely. Good conditions today."
    else:
        result["recommendation"] = "Borderline day. Stay intentional about movement."

    return result

# Test with three different days
scenarios = [
    (5, 8, 60, "Leuyan Lepario"),
    (8, 8, 75, "Brian Kamau"),
    (9.0, 6, 65, "Grace Achieng"),
]

for sleep, water, bench, name in scenarios:
    r = predict_day(sleep, water, bench)
    outcome = "Goal hit" if r["hit_goal"] else "Below goal"
    print(f"{name}: {outcome} ({r['confidence']}% confidence)")
    print(f"  {r['recommendation']}")
    print()

