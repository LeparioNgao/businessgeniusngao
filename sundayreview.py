# Write a function called greet that takes a name
# and returns a greeting string
def greet(name):
    return f"Hello, {name}! Welcome to the program."
print(greet("Alice"))  # Example usage
print(greet("Bob"))    # Example usage

# Write a function called power(base, exp=2)
# that returns base raised to exp
def power(base, exp=2):
    return base ** exp
print(power(3))        # Example usage, should return 9
print(power(2, 3))     # Example usage, should return 8

# Use a list comprehension to get all even numbers from 1 to 30
even_numbers = [x for x in range(1, 31) if x % 2 == 0]
print(even_numbers)    # Example usage, should print even numbers from 1 to 30

# Now get the squares of those even numbers
even_squares = [x**2 for x in even_numbers]
print(even_squares)    # Example usage, should print squares of even numbers from 1 to 30

# Write a function that takes a list of scores
# and returns the average, highest, and lowest
def score_summary(scores):
    if not scores:
        return {"average": None, "highest": None, "lowest": None}
    average = sum(scores) / len(scores)
    highest = max(scores)
    lowest = min(scores)
    return {"average": average, "highest": highest, "lowest": lowest}
print(score_summary([88, 92, 79, 95, 85]))

def greet(name):
    return f"Hello, {name}!"

print(greet("Amerix"))
print(greet("SMP Member"))
print(greet("Guest"))
