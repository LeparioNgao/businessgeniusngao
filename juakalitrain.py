#Evaluation metrics work the same regardless of what you are predicting.
# Below is a classifier predicting whether a Jua Kali welding job will be paid, based on quote amount and job type.
# The same precision, recall, and F1 logic applies.

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Features: [quote_kes, job_type_encoded]
# Job types: gate=0, window grills=1, door frame=2, roof sheet=3
# Label: 1 = paid, 0 = pending/unpaid
X = np.array([
    [28000,0],[14500,1],[9800,2],[32000,0],[12000,1],
    [18500,0],[11000,2],[29500,0],[8500,3],[22000,1],
    [35000,0],[7200,2],[16000,3],[31000,0],[13500,1],
    [10500,2],[24000,0],[9000,3],[27000,1],[15000,2],
])
y = np.array([1,1,0,1,1,0,1,1,1,0,1,0,1,1,0,1,1,0,1,0])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("Job payment prediction report:")
print(classification_report(y_test, y_pred, target_names=["Unpaid", "Paid"]))

# A confusion matrix compares the actual test labels with the model's predictions.
# Rows represent actual labels; columns represent predicted labels.
cm = confusion_matrix(y_test, y_pred)
print("Confusion matrix:")
print("              Predicted Unpaid  Predicted Paid")
print(f"Actual Unpaid {cm[0][0]:>17}  {cm[0][1]:>15}")
print(f"Actual Paid   {cm[1][0]:>17}  {cm[1][1]:>15}")

# Feature importance shows how useful each feature was to the trained forest.
# The names must stay in the same order as the columns in X.
feature_names = ["quote_kes", "job_type_encoded"]
importances = clf.feature_importances_

print("Feature importances:")
# Pair names with their scores and print the most important feature first.
for name, importance in sorted(zip(feature_names, importances), key=lambda item: -item[1]):
    print(f"  {name:<18} {importance:.3f}")