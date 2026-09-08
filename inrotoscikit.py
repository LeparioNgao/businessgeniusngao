#Machine learning is not magic.
# It is a method: show the model examples, let it find the pattern, then ask it to apply that pattern to new data.
# scikit-learn is the standard library for doing this in Python.
# This lesson shows you the workflow from data to trained model to prediction.

# Learning Objectives
# 1. Understand what machine learning is and when to use it
# 2. Know the difference between supervised and unsupervised learning
# 3. Prepare features (X) and labels (y) for a model
# 4. Split data into training and test sets
# 5. Train a Linear Regression model and make predictions
# 6. Evaluate the model with a score

#scikit-learn installs via micropip in the browser.
# The first Run on this page takes 45 to 60 seconds. After that, all subsequent runs on this page are instant.

# 1. What is Machine Learning?
#Machine learning is training a program to make predictions by showing it examples, rather than writing explicit rules.
# You provide labeled data: inputs with known correct outputs.
# The model finds the mathematical relationship.
# Then it applies that relationship to inputs it has never seen before.

#   Type	                     What It Does	                         Known Example
# Supervised (regression)	    Predicts a number	            Predict bench press from sleep + steps
# Supervised (classification)	Predicts a category	        Predict OMAD vs 2MAD from daily metrics
# Unsupervised (clustering)	    Groups similar records	        Group members by training style

# 1(a): The ML Workflow.
#Every scikit-learn project follows the same five steps.
# Prepare data. Split into train/test. Create the model object. Fit (train) it on training data.
# Evaluate on test data.

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Step 1: Data (28 days of SMP fitness log)
# Features: sleep hours, water glasses, bench press kilograms
# Label: steps taken that day
X = np.array([
    [7.5, 7, 80], [8.0, 8, 82], [6.5, 6, 78], [7.0, 9, 85], [9.0, 8, 80], [7.5, 7, 83], [8.0, 8, 84],
    [6.0, 6, 81], [8.5, 9, 85], [7.0, 8, 80], [7.5, 8, 86], [9.0, 7, 79], [7.0, 9, 84], [7.5, 8, 83],
    [7.0, 7, 82], [8.0, 8, 86], [6.5, 6, 79], [7.5, 9, 88], [8.0, 8, 81], [7.0, 7, 85], [8.5, 9, 87],
    [7.0, 8, 82], [7.5, 8, 86], [6.5, 6, 80], [8.0, 9, 87], [9.5, 7, 79], [7.0, 8, 84], [8.0, 9, 86]
])  # shape: (28, 3) - 28 days, 3 features each

y = np.array([
    9200, 10500, 8800, 11000, 7600, 9400, 10200,
    8900, 10800, 9100, 11200, 7900, 10000, 9700,
    9500, 10300, 8600, 11500, 8200, 9800, 10600,
    9000, 10100, 8400, 10900, 7500, 9600, 10400
])  # shape: (28,) - one step count per day

print(f"Features shape: {X.shape}")
print(f"Labels shape:   {y.shape}")

# Step 2: Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\nTraining rows: {X_train.shape[0]}")
print(f"Test rows:     {X_test.shape[0]}")

# Step 3: Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 4: Evaluate
score = model.score(X_test, y_test)
print(f"\nModel R2 score: {score:.3f}")
print("(1.0 = perfect, 0 = no better than guessing the mean)")

# 2. Making Predictions
#Once trained, the model can predict step counts for days it has never seen, given sleep, water, and bench press.

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X = np.array([[7.5,7,80],[8.0,8,82],[6.5,6,78],[7.0,9,85],[9.0,8,80],[7.5,7,83],[8.0,8,84],[6.0,6,81],[8.5,9,85],[7.0,8,80],[7.5,8,86],[9.0,7,79],[7.0,9,84],[7.5,8,83],[7.0,7,82],[8.0,8,86],[6.5,6,79],[7.5,9,88],[8.0,8,81],[7.0,7,85],[8.5,9,87],[7.0,8,82],[7.5,8,86],[6.5,6,80],[8.0,9,87],[9.5,7,79],[7.0,8,84],[8.0,9,86]])
y = np.array([9200,10500,8800,11000,7600,9400,10200,8900,10800,9100,11200,7900,10000,9700,9500,10300,8600,11500,8200,9800,10600,9000,10100,8400,10900,7500,9600,10400])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# Predict for new days not in the training data
new_days = np.array([
    [8.0, 8, 85],   # 8 hours sleep, 8 glasses water, 85 kg bench press
    [6.0, 5, 75],   # 6 hours sleep, 5 glasses water, 75 kg bench press
    [9.0, 9, 90],   # 9 hours sleep, 9 glasses water, 90 kg bench press
    [7.5, 7, 82],   # typical day
])

predictions = model.predict(new_days)
print("Predictions for new days:")
for i, (inputs, pred) in enumerate(zip(new_days, predictions)):
    sleep, water, bench = inputs
    print(f"  Sleep={sleep}h, Water={water}g, Bench={bench}kg => predicted steps: {pred:,.0f}")

# 3. Classification: Predicting a Category.
#Regression predicts a number. Classification predicts a category.
# Use a Random Forest classifier to predict whether a day will hit the 10,000 step goal based on sleep and water intake.

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X = np.array([[7.5,7,80],[8.0,8,82],[6.5,6,78],[7.0,9,85],[9.0,8,80],[7.5,7,83],[8.0,8,84],[6.0,6,81],[8.5,9,85],[7.0,8,80],[7.5,8,86],[9.0,7,79],[7.0,9,84],[7.5,8,83],[7.0,7,82],[8.0,8,86],[6.5,6,79],[7.5,9,88],[8.0,8,81],[7.0,7,85],[8.5,9,87],[7.0,8,82],[7.5,8,86],[6.5,6,80],[8.0,9,87],[9.5,7,79],[7.0,8,84],[8.0,9,86]])
steps = np.array([9200,10500,8800,11000,7600,9400,10200,8900,10800,9100,11200,7900,10000,9700,9500,10300,8600,11500,8200,9800,10600,9000,10100,8400,10900,7500,9600,10400])

# Convert step counts to binary labels: 1 = hit goal, 0 = missed
y = (steps >= 10000).astype(int)
print("Label distribution (1=hit goal, 0=missed):")
print(f"  Hit goal:  {y.sum()}/28 days")
print(f"  Missed:    {(y==0).sum()}/28 days")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)
print(f"\nClassification accuracy: {accuracy:.0%}")

# Predict new days
new_days = np.array([[8.0, 8, 85], [6.0, 5, 75], [9.0, 9, 90]])
preds = clf.predict(new_days)
labels = {1: "Goal hit", 0: "Below goal"}
print("\nPredictions for new days:")
for inputs, pred in zip(new_days, preds):
    print(f"  Sleep={inputs[0]}h, Water={int(inputs[1])}g, Bench={int(inputs[2])}kg => {labels[pred]}")

#Random Forest builds many decision trees and combines their votes.
# It handles non-linear patterns better than Linear Regression and is less prone to overfitting than a single decision tree.

