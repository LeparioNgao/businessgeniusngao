my_log = {
    "steps": 4500,
    "water_glasses": 8,
    "fasting_protocol": "OMAD",
    "cold_shower": True,
    "sleep_hours": 8,
}

for key, value in my_log.items():
    print(key, ":", value)

if my_log["steps"] >= 8000:
    print("Great job! You reached your step goal for the day.")
else:
    print("Step goal not reached.")