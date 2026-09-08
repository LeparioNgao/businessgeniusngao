client = [
    {
        "name": "John",
        "steps": [8500, 6200, 9600, 11000, 14000, 8000, 7550]
    },
    {
        "name": "Kelvin",
        "steps": [9600, 14350, 7200, 9900, 10300, 8800, 10850]
    },
    {
        "name": "Synthia",
        "steps": [6750, 8890, 9900, 10500, 11300, 12500, 7890]
    },
    {
        "name": "Jayden",
        "steps": [9990, 8850, 10340, 6580, 16500, 12400, 10500]
    },
]

#A list of all steps above 10000 from any person
goal_days = [s for person in client for s in person["steps"] if s >= 10000]
print("\nSteps above 10000:", goal_days)

#Names with average steps above 9000
high_average_names = [person["name"] for person in client if sum(person["steps"])/ len(person["steps"]) >9000]
print(high_average_names)