#string variable
name1 = "Lepario Leuyan"
#integer variable
age = 26
#string varaible
occupation = "Roofer"
#string variable
company = "Ngao Roofing"

print(f"My name is {name1}. I am {age} years old and I work as a {occupation} at {company}.")

#string text exercise
name2 = "Eric"
brand = "Amerix"
message = "Discipline. Order. Consistency."

print(f"My name is {name2}. I own {brand} and my message is '{message}'.")

#integer exercise
age = 44
cold_shower_streak = 30
followers = 23000000

print(age + 1)

#float exercise
weight_kg = 82.5
height_m = 1.78
body_fat_pct = 0.14

print(weight_kg * body_fat_pct)

#Boolean exercise
morning_workout_done = True
skipped_gym = False
cold_shower_done = True

print(morning_workout_done and cold_shower_done)
print(type("Ngao Roofing"))

#Operators exercise
a = 10
b = 3

print(a + b)
print(a - b)
print(a * b)
print(a / b)
print(a // b)
print(a % b)
print(a ** b)

#ask the user for their name and age
user_name = input("What is your name? ")
user_age = input("What is your age? ")
print(f"Hello {user_name}, you are {user_age} years old.")

#converting Input to numbers
#This would fail: "5" + "5" = "55"
#This would work: int("5") + int("5") = 10

first = input("Enter the first number: ")
second = input("Enter the second number: ")

#convert strings to intergers before calculating
first_num = int(first)
second_num = int(second)

print(f"Sum: {first_num + second_num}")
print(f"Difference: {first_num - second_num}")
print(f"Product: {first_num * second_num}")
print(f"Quotient: {first_num / second_num}")

#Handling bad input
user_input = input("Enter a number: ")

try:
    user_number = int(user_input)
    print(f"You entered the number: {user_number}")
except ValueError:
    print("That's not a valid number. Please try again.")