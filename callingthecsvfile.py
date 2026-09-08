import joblib

if __name__ == "__main__":
    clf = joblib.load("smp_coach_model.pkl")

    features = [[8.0, 10, 90]]
    prediction = clf.predict(features)
    probabilities = clf.predict_proba(features)

    if prediction[0] == 1:
        label = "HIT GOAL"
    else:
        label = "MISS GOAL"

    print("Feature array:", features)
    print("Prediction array:", prediction)
    print("Probability array:", probabilities)
    print(f"Model prediction: {label}")
    print(f"Confidence: {probabilities[0][prediction[0]]:.2%}")