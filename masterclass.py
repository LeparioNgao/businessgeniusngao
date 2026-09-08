#JSON is a text-based data format. It uses curly braces for objects (like Python dicts), square brackets for arrays (like Python lists), and strings must use double quotes. Python's built-in json module converts between JSON text and Python data structures.
#json.dumps() takes a Python dictionary or list and converts it into a JSON-formatted string. The s stands for "string".

import json

daily_log = {
    "steps": 9200,
    "water_glasses": 8,
    "cold_shower": True,
    "fasting_protocol": "OMAD",
    "sleep_hours": 7.5
}

# Convert to JSON string
json_text = json.dumps(daily_log)
print("Type:", type(json_text))
print("JSON:", json_text)

# Pretty print with indentation
pretty = json.dumps(daily_log, indent=2)
print("\nPretty JSON:")
print(pretty)

#Tip: indent=2 adds line breaks and indentation to make the output readable. Use it when printing JSON for humans. Leave it out when sending data to an API.

#json.loads() takes a JSON string and converts it back into Python data (a dictionary or list). This is what you use when you receive data from an API.

import json

# This is what an API response might look like
api_response = '{"steps": 10500, "water_glasses": 9, "cold_shower": true, "protocol": "Autophagy Marathon"}'

# Convert JSON string to Python dictionary
data = json.loads(api_response)

print("Type:", type(data))
print("Steps:", data["steps"])
print("Water glasses:", data["water_glasses"])
print("Cold shower:", data["cold_shower"])
print("Protocol:", data["protocol"])



#Working with JSON files.
#In VS Code, you use json.dump() (no s) to write to a file and json.load() (no s) to read from one. The interactive terminals here simulate this using in-memory strings.

# Writing JSON to a file (use in VS Code):
with open("log.json", "w") as f:
    json.dump(daily_log, f, indent=2)

# Reading JSON from a file (use in VS Code):
with open("log.json", "r") as f:
    data = json.load(f)


daily_logs = {
    "steps": 16500,
    "water_glasses": 12,
    "protocol": "2MAD",
    "cold_shower": False,
    "sleep_hours": 8
}

with open("log.json", "w") as f:
    json.dump(daily_logs, f, indent=2)

with open("log.json", "r") as f:
    data = json.load(f)

#Navigating nested JSON:

api_json = '''
{
  "client": "James Omondi",
  "week": 1,
  "daiily_logs": [
    {"day": "Monday",    "steps": 9200,  "protocol": "OMAD"},
    {"day": "Tuesday",   "steps": 10500, "protocol": "2MAD"},
    {"day": "Wednesday", "steps": 8800,  "protocol": "OMAD"},
    {"day": "Thursday",  "steps": 11000, "protocol": "Autophagy Marathon"},
    {"day": "Friday",    "steps": 7600,  "protocol": "OMAD"},
    {"day": "Saturday",  "steps": 12000, "protocol": "2MAD"},
    {"day": "Sunday",    "steps": 9500,  "protocol": "OMAD"}
  ]
}
'''
data = json.loads(api_json)
print("Client:", data["client"])
print("Week:", data["week"])
print()

for log in data["daiily_logs"]:
    status = "✅" if log["steps"] >= 8000 else "❌"
    print(f"  {log['day']}: {log['steps']} steps, {log['protocol']} {status}")


#JSON and Error Handling:
#When you receive JSON from an API, it may not be valid. Use try/except to catch errors when parsing JSON. The json module raises a json.JSONDecodeError if the string is not valid JSON.
responses = [
    '{"steps": 9200, "protocol": "OMAD"}',
    'not valid json at all',
    '{"steps": 10500, "protocol": "2MAD"}'
]

for r in responses:
    try:
        data = json.loads(r)
        print(f"Parsed OK: {data['steps']} steps")
    except json.JSONDecodeError:
            print(f"Invalid JSON: {r[:30]}...")
