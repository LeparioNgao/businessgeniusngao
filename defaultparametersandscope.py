#A default parameter is written as parameter=value in the function definition. It gives the parameter a fallback value. You only need to pass an argument for that parameter when you want a different value.
def check_steps(steps, goal = 8000):
    if steps >= goal:
        print(f"{steps} steps - Goal of {steps} hit.")
    else:
        print(f"{steps} steps - Goal of {steps} missed.")

#use the default parameter
check_steps(9200)
check_steps(7500)

#override the default parameter
check_steps(9800, goal = 10000)
check_steps(11500, goal = 10000)

#Multiple default parameters.
def log_day(steps, water = 8, protocol = "OMAD"):
    print(f"\nSteps: {steps} | Water: {water} glasses | Protocol: {protocol}")

log_day(9300) #uses both defaults
log_day(10500, water = 9) #override water only
log_day(8800, water = 7, protocol = "2MAD") #override both

#Keyword arguments
def client_report(name, goal, session = 4, bench_kg = 60):
    print(f"\n{name} | Goal: {goal} | Sessions/week: {session} | Bench: {bench_kg} kg")

#positional arguments
client_report("James", "fat loss")

#keyword arguments: order does not matter
client_report(goal = "muscle gain", name = "Mwangi", bench_kg = 100)

#Mix of positional and keyword
client_report("Sandra", "endurance", bench_kg = 50)

#Local scope: a variable created inside a function. It only exists while the function is running. It disappears when the function ends.
#Global scope: a variable created outside all functions. It exists for the entire program and can be read inside functions.
step_goal = 8000 #Global variable
def check_today(steps):
    result = "hit" if steps >= step_goal else "missed"
    print(f"\nGoal {result}: {steps} steps")
check_today(9200)
check_today(7000)

#writing print(result) would give an error - because result does not exist outside its scope.

#Functions can read global variables, but they cannot change them without using the global keyword. In practice, pass values as parameters rather than relying on global variables. It keeps functions independent and predictable.
def calculate_bmi(weight_kg, height_m):
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

weight = 84
height = 1.78
bmi = calculate_bmi(weight, height)
category = bmi_category(bmi)

print(f"\nWeight: {weight} kg | Height: {height} m")
print(f"\nBMI: {bmi} | Category: {category}")