#A model that scores 90% accuracy sounds impressive until you learn that 90% of the data was in one class anyway.
# Evaluation is about understanding what a score actually means.
# This lesson covers the metrics that tell you whether your model is genuinely working or just guessing the majority class.

#Learning Objectives
# 1. Understand the train/test split and why it matters
# 2. Read and interpret accuracy, precision, recall, and F1 score
# 3. Understand and build a confusion matrix
# 4. Check feature importances to understand what the model learned
# 5. Compare two algorithms on the same dataset

# 1. Why Evaluation matters.

#Evaluation measures how well a model generalizes to data it has never seen.
# You train on one portion of the data and test on the rest.
# A model that only memorizes training examples (overfits) will score high on training data and poorly on test data.
# Evaluation catches this.



# 2. Accuracy, Precision, and Recall.

# Accuracy is the percentage of correct predictions overall.
# It misleads when classes are imbalanced (90 out of 100 records belong to one class; always guessing that class gives 90% accuracy but the model learns nothing).
# Precision is: of all predictions that said "yes", how many were actually yes?
# Recall is: of all the actual "yes" cases, how many did the model find?
# F1 is the harmonic mean of precision and recall.

# NumPy stores the example data in arrays that scikit-learn can use.
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Each row is one person's input data.
# The three columns are: hours of sleep, glasses of water, and bench press weight.
X = np.array([
    [7.5,7,80],[8.0,8,82],[6.5,6,78],[7.0,9,85],[9.0,8,80],[7.5,7,83],[8.0,8,84],
    [6.0,6,81],[8.5,9,85],[7.0,8,80],[7.5,8,86],[9.0,7,79],[7.0,9,84],[7.5,8,83],
    [7.0,7,82],[8.0,8,86],[6.5,6,79],[7.5,9,88],[8.0,8,81],[7.0,7,85],[8.5,9,87],
    [7.0,8,82],[7.5,8,86],[6.5,6,80],[8.0,9,87],[9.5,7,79],[7.0,8,84],[8.0,9,86]
])
# Create the label the model should learn to predict.
# A value of 1 means the person reached at least 10,000 steps; 0 means they did not.
steps = np.array([9200,10500,8800,11000,7600,9400,10200,8900,10800,9100,11200,7900,10000,9700,9500,10300,8600,11500,8200,9800,10600,9000,10100,8400,10900,7500,9600,10400])
y = (steps >= 10000).astype(int)

# Keep most records for learning and reserve 25% for testing on unseen examples.
# random_state makes the split reproducible each time the script runs.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Build a random forest from 20 decision trees.
# The fixed random_state makes the model's result reproducible as well.
clf = RandomForestClassifier(n_estimators=20, random_state=42)
# Learn the relationship between the three features and the 0/1 target labels.
clf.fit(X_train, y_train)
# Predict the labels for the test features the model did not train on.
y_pred = clf.predict(X_test)

# Compare the predictions with the true test labels using several metrics.
# target_names gives the numeric classes readable names in the report.
print("Classification report:")
print(classification_report(y_test, y_pred, target_names=["Below 10k", "Hit 10k"]))

# 3. Confusion Matrix

# A confusion matrix shows the count of correct and incorrect predictions, broken down by class.
# Rows are actual labels; columns are predicted labels.
# The diagonal is correct predictions. Off-diagonal entries are errors.

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

X = np.array([[7.5,7,80],[8.0,8,82],[6.5,6,78],[7.0,9,85],[9.0,8,80],[7.5,7,83],[8.0,8,84],[6.0,6,81],[8.5,9,85],[7.0,8,80],[7.5,8,86],[9.0,7,79],[7.0,9,84],[7.5,8,83],[7.0,7,82],[8.0,8,86],[6.5,6,79],[7.5,9,88],[8.0,8,81],[7.0,7,85],[8.5,9,87],[7.0,8,82],[7.5,8,86],[6.5,6,80],[8.0,9,87],[9.5,7,79],[7.0,8,84],[8.0,9,86]])
steps = np.array([9200,10500,8800,11000,7600,9400,10200,8900,10800,9100,11200,7900,10000,9700,9500,10300,8600,11500,8200,9800,10600,9000,10100,8400,10900,7500,9600,10400])
y = (steps >= 10000).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
clf = RandomForestClassifier(n_estimators=20, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Arrange the test results into a 2x2 table of actual labels versus predictions.
# With labels 0 and 1, rows are actual Below/Hit and columns are predicted Below/Hit.
cm = confusion_matrix(y_test, y_pred)
print("\nConfusion matrix:")
# Print column headings so the four numbers are easy to read.
print(f"                Predicted Below  Predicted Hit")
# cm[row][column] selects one cell from the matrix.
# For example, cm[0][1] means actual Below, predicted Hit.
print(f"Actual Below    {cm[0][0]:>14}  {cm[0][1]:>14}")
print(f"Actual Hit      {cm[1][0]:>14}  {cm[1][1]:>14}")
print()
# The diagonal cells are correct predictions: cm[0][0] and cm[1][1].
# The off-diagonal cells are mistakes: cm[0][1] and cm[1][0].
print(f"True Negatives  (correct 'Below'):  {cm[0][0]}")
print(f"False Positives (wrong 'Hit'):       {cm[0][1]}")
print(f"False Negatives (missed 'Hit'):      {cm[1][0]}")
print(f"True Positives  (correct 'Hit'):     {cm[1][1]}")


# 4. Feature Importance.

# Random Forest can tell you which features it relied on most when making predictions.
# Higher importance means the model found that feature more useful for splitting the data correctly.

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X = np.array([[7.5,7,80],[8.0,8,82],[6.5,6,78],[7.0,9,85],[9.0,8,80],[7.5,7,83],[8.0,8,84],[6.0,6,81],[8.5,9,85],[7.0,8,80],[7.5,8,86],[9.0,7,79],[7.0,9,84],[7.5,8,83],[7.0,7,82],[8.0,8,86],[6.5,6,79],[7.5,9,88],[8.0,8,81],[7.0,7,85],[8.5,9,87],[7.0,8,82],[7.5,8,86],[6.5,6,80],[8.0,9,87],[9.5,7,79],[7.0,8,84],[8.0,9,86]])
steps = np.array([9200,10500,8800,11000,7600,9400,10200,8900,10800,9100,11200,7900,10000,9700,9500,10300,8600,11500,8200,9800,10600,9000,10100,8400,10900,7500,9600,10400])
y = (steps >= 10000).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
clf = RandomForestClassifier(n_estimators=20, random_state=42)
clf.fit(X_train, y_train)

# Give each column in X a readable name, in the same order as the columns appear in the data.
feature_names = ["sleep_hours", "water_glasses", "bench_press_kg"]
# The trained forest calculates one importance score for each feature.
# The scores are in the same order as feature_names and usually add up to 1.0.
importances = clf.feature_importances_

print("\nFeature importances (how much each feature contributes):")
# Pair each feature name with its score, then sort from most to least important.
for name, imp in sorted(zip(feature_names, importances), key=lambda x: -x[1]):
    # Scale the score into a small text bar so the values are easier to compare visually.
    bar = "#" * int(imp * 40)
    print(f"  {name:<18} {imp:.3f}  {bar}")

# Feature importance does not mean causation. It means the model found this feature useful for splitting the data.
# In small datasets, importances can be noisy. Always look at whether the relationships make logical sense.


# 5. Comparing Two Algorithms.

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

X = np.array([[7.5,7,80],[8.0,8,82],[6.5,6,78],[7.0,9,85],[9.0,8,80],[7.5,7,83],[8.0,8,84],[6.0,6,81],[8.5,9,85],[7.0,8,80],[7.5,8,86],[9.0,7,79],[7.0,9,84],[7.5,8,83],[7.0,7,82],[8.0,8,86],[6.5,6,79],[7.5,9,88],[8.0,8,81],[7.0,7,85],[8.5,9,87],[7.0,8,82],[7.5,8,86],[6.5,6,80],[8.0,9,87],[9.5,7,79],[7.0,8,84],[8.0,9,86]])
steps = np.array([9200,10500,8800,11000,7600,9400,10200,8900,10800,9100,11200,7900,10000,9700,9500,10300,8600,11500,8200,9800,10600,9000,10100,8400,10900,7500,9600,10400])
y = (steps >= 10000).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

models = {
    "Decision Tree":    DecisionTreeClassifier(random_state=42),
    "Random Forest":    RandomForestClassifier(n_estimators=20, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=200),
}

print("Model comparison:")
print(f"  {'Model':<25} {'Accuracy':>10}")
print(f"  {'-'*36}")
for name, model in models.items():
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    print(f"  {name:<25} {acc:>10.0%}")