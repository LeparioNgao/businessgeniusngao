#Suppose you have a list of step counts for the week and you want a new list that contains only the days where you hit 8,000 steps. The standard way uses a loop:

weekyly_steps = [9200, 7500, 10500, 8800, 6900, 11000, 9600]
goal_days = []
for steps in weekyly_steps:
    if steps >= 8000:
        goal_days.append(steps)
print(goal_days)

#Python has a shorter way of running the same thing:
#A list comprehension is a one-line way to build a new list from an existing one. The format is: [expression for item in iterable if condition]. The if condition part is optional. It creates a new list without changing the original.
week_steps = [9700, 15000, 6800, 10780, 7500, 9200, 8100]
goal_days = [steps for steps in week_steps if steps >= 8000]
print(goal_days)

#convert each step count to km
km_walked = [ round(s * 1.3 / 1000, 2) for s in week_steps]
print("\nSteps:", week_steps)
print("\nkm:", km_walked)

#Filtering a list of dictionaries
clients = [
    {
        "name": "James",
        "goal": "fat loss",
        "sessions": 4
    },
    {
        "name": "Mwangi",
        "goal": "muscle gain",
        "sessions": 5
    },
    {
        "name": "Sandra",
        "goal": "Endurance",
        "sessions": 3
    },
    {
        "name": "Patrick",
        "goal": "muscle gain",
        "sessions": 4
    },
    {
        "name": "Grace",
        "goal": "fat loss",
        "sessions": 3
    },
]

#Get names of all fat loss clients
fat_loss_name = [c["name"] for c in clients if c["goal"] == "fat loss"]
print("\nFat loss clients: ", fat_loss_name)

#Get all clients with four or more sessions per week
active_clients = [c for c in clients if c["sessions"]>= 4]
print("\nActive clients: ", [c["name"] for c in active_clients])

#Build a status list

statuses = ["Goal hit" if s >= 8000 else "Below goal" for s in week_steps]
for i, status in enumerate(statuses):
    print(f"\nDay {i + 1}: {week_steps[i]} steps - {status}")