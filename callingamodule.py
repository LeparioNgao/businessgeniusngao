import joblib
import numpy as np

clf = joblib.load("step_goal_model.joblib")

# Predict without retraining
new_day = np.array([[8.0, 8, 84]])
pred = clf.predict(new_day)[0]
print("Prediction:", "Goal hit" if pred == 1 else "Below goal")