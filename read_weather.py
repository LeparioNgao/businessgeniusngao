import json

with open("nairobi_weather.json", "r") as f:
    data = json.load(f)

print(f"Nairobi temperature: {data['main']['temp']} C")