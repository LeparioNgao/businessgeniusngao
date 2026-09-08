week_log = [
    {"day": "Monday",
     "steps": 7500,
     "protocol": "OMAD",
    },
    {
        "day": "Tuesday",
        "steps": 13000,
        "protocol": "2MAD",
    },
    {
        "day": "Wednesday",
        "steps": 9700,
        "protocol": "2MAD",
    },
    {
        "day": "Thursday",
        "steps": 10000,
        "protocol": "Autophagy Marathon",
    },
    {
        "day": "Friday",
        "steps": 8500,
        "protocol": "OMAD",
    },
]
#loop that prints each days details
total = 0
for log in week_log:
    print(log["day"], "|", log["steps"], "|", log["protocol"])
    total += log["steps"]

average = total / len(week_log)
print("Average step for the week:", average)

