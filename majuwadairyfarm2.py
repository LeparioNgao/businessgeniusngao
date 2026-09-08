"""Majuwa Dairy Farm: a small, end-to-end ML decision-support example.

This is a teaching simulation, not a replacement for a vet, nutritionist,
or farm accountant. Real predictions need the farm's own cleaned records.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
rng = np.random.default_rng(RANDOM_STATE)

# Each historical row represents one cow on one day.
# Features: feed kg, lactation day, temperature, and previous milk litres.
cow_count = 40
days = 180
cow_ids = np.repeat(np.arange(1, cow_count + 1), days)
day_numbers = np.tile(np.arange(1, days + 1), cow_count)
lactation_day = rng.integers(10, 260, size=len(cow_ids))
feed_kg = np.clip(5.5 + lactation_day * 0.008 + rng.normal(0, 0.45, len(cow_ids)), 4.5, 9.5)
temperature_c = rng.normal(24, 3, len(cow_ids))
previous_milk_l = np.clip(
    8 + feed_kg * 1.25 - lactation_day * 0.012
    - np.maximum(temperature_c - 27, 0) * 0.35
    + rng.normal(0, 0.9, len(cow_ids)),
    3,
    22,
)

# These outcomes stand in for measurements that a real farm would collect.
milk_l = np.clip(
    previous_milk_l + feed_kg * 0.38 - lactation_day * 0.004
    - np.maximum(temperature_c - 27, 0) * 0.18
    + rng.normal(0, 0.65, len(cow_ids)),
    2,
    28,
)
health_event = (
    (feed_kg < 6.2).astype(int)
    + (temperature_c > 29).astype(int)
    + (previous_milk_l - milk_l > 2.0).astype(int)
    + rng.binomial(1, 0.04, len(cow_ids))
    >= 2
).astype(int)

features = np.column_stack(
    [feed_kg, lactation_day, temperature_c, previous_milk_l]
)

# Keep the test records hidden while training, then measure generalisation.
X_train, X_test, milk_train, milk_test, health_train, health_test = train_test_split(
    features, milk_l, health_event, test_size=0.2, random_state=RANDOM_STATE
)

milk_model = RandomForestRegressor(n_estimators=80, random_state=RANDOM_STATE)
health_model = RandomForestClassifier(
    n_estimators=80, class_weight="balanced", random_state=RANDOM_STATE
)
milk_model.fit(X_train, milk_train)
health_model.fit(X_train, health_train)

milk_error = mean_absolute_error(milk_test, milk_model.predict(X_test))
health_accuracy = accuracy_score(health_test, health_model.predict(X_test))


def predict_cow(feed_kg, lactation_day, temperature_c, previous_milk_l):
    """Predict one cow's milk yield and health-alert probability."""
    inputs = np.array([[feed_kg, lactation_day, temperature_c, previous_milk_l]])
    expected_milk = milk_model.predict(inputs)[0]
    alert_probability = health_model.predict_proba(inputs)[0, 1]
    return expected_milk, alert_probability


def forecast_demand(days_ahead=7):
    """Estimate milk available for sale and feed required for the herd."""
    forecast = []
    for future_day in range(days + 1, days + days_ahead + 1):
        herd_rows = []
        for cow_id in range(cow_count):
            row = features[cow_id * days + (days - 1)].copy()
            row[1] += 1  # lactation progresses by one day
            row[2] = 24 + 3 * np.sin(future_day / 10)
            herd_rows.append(row)
        predicted_milk = milk_model.predict(np.array(herd_rows)).sum()
        feed_required = np.array(herd_rows)[:, 0].sum()
        forecast.append((future_day, predicted_milk, feed_required))
    return forecast


print("MAJUWA DAIRY FARM | ML OPERATIONS REPORT")
print("=" * 48)
print(f"Herd: {cow_count} cows | Historical records: {len(features):,}")
print(f"Milk model: average error {milk_error:.2f} litres per cow/day")
print(f"Health model: test accuracy {health_accuracy:.0%}")

print("\nINDIVIDUAL COW CHECKS")
for cow_id in (1, 12, 27):
    row = features[(cow_id - 1) * days + days - 1]
    expected_milk, alert_probability = predict_cow(*row)
    action = "Inspect today" if alert_probability >= 0.35 else "Normal monitoring"
    print(
        f"Cow {cow_id:02d}: {expected_milk:.1f} L expected | "
        f"health risk {alert_probability:.0%} | {action}"
    )

print("\nSEVEN-DAY SALES AND FEED FORECAST")
for future_day, predicted_milk, feed_required in forecast_demand():
    print(
        f"Day {future_day}: {predicted_milk:,.0f} L milk | "
        f"{feed_required:,.0f} kg feed"
    )

# A manager can use these outputs to plan buyers, feed orders, and inspections.
weekly_milk = sum(item[1] for item in forecast_demand())
weekly_feed = sum(item[2] for item in forecast_demand())
print("\nMANAGER'S PLANNING TOTALS")
print(f"Expected milk to sell: {weekly_milk:,.0f} L")
print(f"Feed to prepare/order: {weekly_feed:,.0f} kg")
print("Health alerts are priorities for inspection, not diagnoses.")
