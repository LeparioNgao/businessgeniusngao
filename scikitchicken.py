#Below is a classifier that predicts whether a chicken pen will hit 300 eggs for the week, based on daily feed and deaths recorded.
# Same fit/predict pattern, different data.

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# X is the input data. Each row represents one past week for the chicken pen.
# The two columns are always in this order: [feed_kg, deaths].
# In machine learning, these input columns are called features.
X = np.array([
    [18.5, 0], [18.0, 1], [19.2, 0], [18.8, 0], [17.5, 2],
    [18.6, 0], [19.0, 0], [20.1, 0], [17.2, 3], [19.5, 0],
    [18.3, 1], [19.8, 0], [17.0, 2], [18.7, 0], [20.0, 0],
    [16.8, 4], [19.1, 0], [18.4, 0], [17.9, 1], [19.6, 0],
])

# y is the correct answer for each week in X, in the same row order.
# 1 means the pen reached the target of 300 eggs; 0 means it did not.
# The model will look for a relationship between each row in X and its y value.
y = np.array([1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1])

# Keep some weeks hidden while training. The model learns from 15 weeks and
# is tested on the remaining 5 weeks, which imitates predicting a future week.
# random_state makes the same weeks go into each group every time we run it.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# A random forest is a group of decision trees. Each tree asks simple questions
# such as whether feed is above a threshold or deaths are below a threshold.
# The forest combines the trees' votes to make the final 0-or-1 prediction.
clf = RandomForestClassifier(n_estimators=10, random_state=42)

# Training means showing the model the known examples and their correct answers.
clf.fit(X_train, y_train)

# score() sends the unseen test rows through the trained model, compares its
# predictions with y_test, and returns the fraction predicted correctly.
accuracy = clf.score(X_test, y_test)
print(f"Model accuracy: {accuracy:.0%}")

# These are new weeks whose outcomes are unknown. They have the same feature
# order as X: feed first, deaths second.
new_weeks = np.array([
    [19.0, 0],  # good feed, no deaths
    [17.0, 3],  # low feed, 3 deaths
    [18.5, 1],  # normal feed, 1 death
])

# predict() applies the pattern learned during fit() to each new row.
preds = clf.predict(new_weeks)

# Convert the model's numeric output into a sentence a person can understand.
labels = {1: "Hit 300 eggs", 0: "Below target"}
print("\nPredictions:")

# zip() pairs each input row with its corresponding prediction.
# inputs[0] is feed, inputs[1] is deaths, and pred is 0 or 1.
for inputs, pred in zip(new_weeks, preds):
    print(f"  Feed={inputs[0]}kg  Deaths={int(inputs[1])} => {labels[pred]}")