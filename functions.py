#A function is a resusable block of code with a name. You create it using def followed by the name and parentheses.

def show_daily_goal():
    print("Step goal: 8000 steps.")
    print("Water goal: 8 glasses.")
    print("Cold Shower: Yes.")

#Call the function
show_daily_goal()
print("\n---")
show_daily_goal()

#A parameter is a variable inside the function that receives a value when you call it.

def check_steps(steps):
    if steps >=10000:
        print(steps, "steps - Goal exceeded.")
    elif steps >=8000:
        print(steps, "steps - Goal Hit.")
    else:
        print(steps, "steps - Below goal.")


#call with different values
check_steps(9200)
check_steps(7500)
check_steps(11000)

#You can have multiple parameters. Separate them with commas in both the definition and the call
def log_day(day, steps, protocol):
    print(f"{day}: {steps} steps | Protocol: {protocol}")
log_day("Monday", 9200, "OMAD")
log_day("Tuesday", 7500, "2MAD")
log_day("Wednesday", 10500, "Autophagy Marathon")

#A fucntion can send a value back to the code that called it. Use the return keyword. Once python hits return, the function stops and the value is sent back.
def calculate_average_steps(steps_list):
    total = sum(steps_list)
    average = total / len(steps_list)
    return average

weekly_steps = [9200, 10500, 8800, 11000, 7600, 9400, 10200]
avg = calculate_average_steps(weekly_steps)
print("Average steps this week:", avg)

def get_status(steps):
    if steps >= 10000:
        print(steps, "steps: Goal exceeded.")
    elif steps >= 8000:
        print(steps, "steps: Goal reached successfully.")
    else:
        print(steps, "steps: Below goal.")

get_status(6500)
get_status(14000)
get_status(8250)

#A fucntion that works with dictionaries.

def print_client(client):
    print(f"Name : {client['name']}")
    print(f"Goal : {client['goal']}")
    print(f"Bench : {client['bench_press_kg']}")
    print(f"Sessions : {client['weekly_sessions']}")
    print()

clients = [
    {
        "name" : "James",
        "goal" : "Fat loss",
        "bench_press_kg" : 80,
        "weekly_sessions": 4
    },
    {
        "name" : "Sandra",
        "goal" : "Endurance",
        "bench_press_kg" : 50,
        "weekly_sessions" : 3
    },
    {
        "name" : "Mwangi",
        "goal" : "Muscle gain",
        "bench_press_kg" : 100,
        "weekly_sessions" : 5
    },
]
for client in clients:
    print_client(client)