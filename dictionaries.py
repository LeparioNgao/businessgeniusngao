#Creating a dictionary
daily_log = {
    "steps": 9200,
    "water_glasses": 8,
    "cold_shower": True,
    "fasting_protocol": "OMAD",
    "sleep_hours": 7.5,
    "junk_entry": "Delete me",
    }
print("Daily Log:", daily_log)

#To read a value from a dictionary, write the dictionary name followed by the key in square brackets. This is similar to accessing a list item, but instead of a number you use the key name.
print("Steps taken today:", daily_log["steps"])
print("Water glasses consumed today:", daily_log["water_glasses"])
print("Cold Shower:", daily_log["cold_shower"])
print("Fasting protocol:", daily_log["fasting_protocol"])
print("Sleep hours:", daily_log["sleep_hours"])

print("Sleep hours:", daily_log.get("sleep_hours"))  # This will return the value associated with the key "sleep_hours"

#Add a new key-value pair to the dictionary
daily_log["pages_read"] = 30  # Adding a new key-value pair to the dictionary
print("After adding pages_read:", daily_log)

#Update an existing value in the dictionary
daily_log["steps"] = 10400  # Updating the value associated with the key "steps"
print("After updating steps:", daily_log)

#Deleting a key
del daily_log["junk_entry"]  # Deleting the key "junk_entry" from the dictionary
print(daily_log)

#Checking if a key exists in the dictionary
if "steps" in daily_log:
    print("Steps recorded:", daily_log["steps"])

if "junk_entry" not in daily_log:
    print("Junk entry does not exist in the dictionary.")

#Loop through the dictionary to print all key-value pairs
for key, value in daily_log.items():
    print(key, ":", value)

for key in daily_log.keys():
    print("Key:", key)

for value in daily_log.values():
    print("Value:", value)

#A Practical Example: Using a dictionary to store and analyze daily health data
client = {
    "name": "James",
    "weight_kg": 84.5,
    "goal": "fat loss",
    "fasting_protocol": "2MAD",
    "bench_press_kg": 80,
    "weekly_sessions": 4,
}

print("Client Profile:")
for key, value in client.items():
    print(f"{key}: {value}")

print()
if client["bench_press_kg"] >= 80:
    print("Bench press goal reached.")