#An exception is an error that occurs while a program is running. Common ones are ValueError (wrong type of value), ZeroDivisionError (dividing by zero), KeyError (key not in dictionary), and FileNotFoundError (file does not exist). Python handles all exceptions the same way: with try and except.

# This will crash
#steps = "nine thousand"
#goal = 8000
#if steps >= goal:  # Can't compare string to number
 #   print("Goal hit")

#try and except will catch the error and allow the program to continue running
try:
    steps = "nine thousand"
    goal = 8000
    if steps >= goal:  # Can't compare string to number
        print("Goal hit")
except TypeError:
    print("Error: Can't compare string to number")

#Another example for try and except
#Wrap code that might fail in a try block. Put your response in the except block. If the try block fails, Python jumps to except instead of crashing.

steps_data = ["9200", "7500", "ten thousand", "8800", "6900"]

for item in steps_data:
    try:
        steps = int(item)
        if steps >= 8000:
            print(steps, "- Goal hit")
        else:
            print(steps, "- Below goal")
    except ValueError:
        print(f"'{item}' is not a valid number. Skipping.")

#Catching multiple exceptions
#Different errors need different responses. You can catch multiple exceptions by using multiple except blocks.
def calculate_average(steps_list):
    try:
        total = sum(steps_list)
        avg = total / len(steps_list)
        return round(avg)
    except ZeroDivisionError:
        print("Error: List is empty. Cannot calculate average.")
        return 0
    except TypeError:
        print("Error: List contains non-numeric values.")
        return 0

print("Average:", calculate_average([9200, 10500, 8800, 11000]))
print("Average:", calculate_average([]))
print("Average:", calculate_average([9200, "eight thousand", 10500]))

#else and finally
#else runs only when no exception occurred. finally runs always, whether an exception occurred or not. Use finally for cleanup actions like closing a file or connection.

def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero.")
    else:
        print(f"{a} / {b} = {result}")
    finally:
        print("(Calculation attempted)")
    print()

safe_divide(100, 4)
safe_divide(100, 0)
safe_divide(9200, 7)

#Raising your own errors
#You can raise your own exceptions with the raise statement. This is useful for validating input or enforcing rules in your code. You can raise built-in exceptions or create your own custom exceptions.
def log_steps(steps):
    if not isinstance(steps, int):
        raise TypeError("Steps must be an integer.")
    if steps < 0:
        raise ValueError("Steps cannot be negative.")
    print(f"Steps logged: {steps}")

try:
    log_steps("nine thousand")
    log_steps(-500)
except ValueError as e:
    print("ValueError:", e)
except TypeError as e:
    print("TypeError:", e)

#Another example of raising an exception
def check_goal(steps, goal):
    if steps < 0:
        raise ValueError("Steps cannot be negative.")
    if goal <= 0:
        raise ValueError("Goal must be a positive number.")
    if steps >= goal:
        print("Goal hit!")
    else:
        print("Goal not reached.")

try:
    check_goal(9200, 0)
    check_goal(-100, 8000)
except ValueError as e:
    print("ValueError:", e)

#EError Handling with Data Processing
#In practice, you use error handling when processing data that may have gaps or inconsistencies. Here is a list of daily logs with some missing or bad values:

daily_logs = [
    {"day": "Monday",    "steps": "9200"},
    {"day": "Tuesday",   "steps": "not recorded"},
    {"day": "Wednesday", "steps": "10500"},
    {"day": "Thursday",  "steps": None},
    {"day": "Friday",    "steps": "8800"},
]

valid_steps = []
for log in daily_logs:
    try:
        steps = int(log["steps"])
        valid_steps.append(steps)
        print(f"{log['day']}: {steps} steps")
    except (ValueError, TypeError):
        print(f"{log['day']}: invalid data - skipped")

if valid_steps:
    avg = sum(valid_steps) / len(valid_steps)
    print(f"\nAverage from valid days: {round(avg)} steps")
