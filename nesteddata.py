#A list of dictionaries
week_log = [
    {
        "day": "Monday",
        "steps": 9200,
        "protocol": "0MAD",
        "cold_shower": True,
    },
    {
        "day": "Tuesday",
        "steps": 10500,
        "protocol": "2MAD",
        "cold_shower": True,
    },
    {
        "day": "Wednesday",
        "steps": 8800,
        "protocol": "0MAD",
        "cold_shower": False,
    },
    {
        "day": "Thursday",
        "steps": 11000,
        "protocol": "Autophagy Marathon",
        "cold_shower": True,
    },
    {
        "day": "Friday",
        "steps": 7600,
        "protocol": "0MAD",
        "cold_shower": True,
    },
]

print(week_log)

#accessing values inside nested data
print(week_log[0]["steps"])  # Accessing steps for Monday
print(week_log[2]["day"])  # Accessing day for Wednesday
print("Tuesday log:", week_log[1])  # Accessing the entire dictionary for Tuesday

#Looping through the list of dictionaries
for log in week_log:
    status = "Goal hit!" if log["steps"] >= 8000 else "Below goal."
    print(log["day"], "-", log["steps"], "steps -", status)

#A for loop to iterate through the list and print if cold shower was taken
for log in week_log:
    if log["cold_shower"]:
        print(log["day"], "took a cold shower.")
    else:
        print(log["day"], "did not take a cold shower.")

#A dictionary with a list as a value
weekly_summary = {
    "week": 1,
    "steps": [9200, 10500, 8800, 11000, 7600, 9400, 10200],
    "protocols": ["OMAD", "2MAD", "OMAD", "Autophagy Marathon", "OMAD", "2MAD", "OMAD"],
    "cold_showers_completed": 6
}
print("Week: ", weekly_summary["week"])
print("Total days tracked: ", len(weekly_summary["steps"]))
print("First day steps: ", weekly_summary["steps"][0])
print("Average steps: ", sum(weekly_summary["steps"])/ len(weekly_summary["steps"]))

#A real world pattern
clients = [
    {"name": "James", "goal": "fat loss", "weekly_sessions": 4, "bench_press_kg": 80},
    {"name": "Mwangi",  "goal": "muscle gain", "weekly_sessions": 5, "bench_press_kg": 100},
    {"name": "Sandra", "goal": "endurance", "weekly_sessions": 3, "bench_press_kg": 50},
    {"name": "Patrick", "goal": "fat loss", "weekly_sessions": 4, "bench_press_kg": 70},
]
print("Fat loss clients:")
for client in clients:
    if client["goal"] == "fat loss":
        print("-", client["name"], "| Bench:", client["bench_press_kg"], "kg | Sessions:", client["weekly_sessions"])