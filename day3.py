#A BMI calculator to get a users BMI from their weight and height
weight = float(input("Enter your weight in kg: "))
height = float(input("Enter your height in meters: "))
bmi = weight / (height ** 2)
print(f"Your BMI is: {bmi: .2f}")

try:
    user_weight = float(input("Enter your weight in kg: "))
    user_height = float(input("Enter your height in meters: "))
    user_bmi = user_weight / (user_height ** 2)
    print(f"Your BMI is: {user_bmi: .2f}")
except ValueError:
    print("Invalid input. Please enter try again.")