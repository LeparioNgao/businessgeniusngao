#Create a Python dictionary called week_report that contains your name, a list of 5 daily step counts, and the fasting protocols used each day. Convert it to a JSON string and print it. Then load it back and compute the average steps from the list inside the JSON.

import json

week_report = {
    "name": "Leuyan Lepario",
    "daily_steps": [12500, 10000, 9000, 8500, 11000],
    "fasting_protocols": ["OMAD", "2MAD", "OMAD", "Autophagy Marathon", "2MAD"]
}

json_string = json.dumps(week_report, indent=2)
print(json_string)

loaded_data = json.loads(json_string)
average_steps = sum(loaded_data["daily_steps"]) / len(loaded_data["daily_steps"])
print(f"\nAverage steps: {average_steps}")