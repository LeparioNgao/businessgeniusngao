#Python comes with hundreds of pre-written tools you can use immediately. You do not build a calculator from scratch. You do not write your own random number generator. You import a module that already has it. This lesson covers three modules you will use constantly: math, random, and datetime.
#A module is a collection of functions and tools packaged into a single file. Use import module_name to load it into your program. Then call functions from it using the format module_name.function_name().
import math

#square root
print("Square root of 144:", math.sqrt(144))

#Round down and round up
print("Floor of 7.9:", math.floor(7.9))
print("Ceiling of 7.1:", math.ceil(7.1))

#Pi
print("Pi:", math.pi)

#Power: 2 to the power of 10
print("2 to the 10th:", math.pow(2, 10))

#A practical use of import math
import math

total_days = 50
training_days_per_week = 5
weeks = total_days / 7

print(f"Total days: {total_days}")
print(f"Full weeks: {math.floor(weeks)}")

#Distance calculation using Pythogoras
walk_east = 3.0 #km
walk_north = 4.0 #km
distance = math.sqrt(walk_east**2 + walk_north**2)
print(f"Direct distance: {distance}km")

#The random module
import random

#Random integer between 1 and 10(inclusive)
print("Random number:", random.randint(1, 10))

#Random float between o and 1
print("Random float:", random.random())

#Random choice from a list
skills = ["welding", "tiling", "upholstery", "phone repair", "copywriting"]
print("Today' skill focus:", random.choice(skills))

#Shuffle a list
random.shuffle(skills)
print("Shuffled:", skills)

#Simulating step counts:
import random

print("\nSimulated step counts for this week:")
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
for day in days:
    steps = random.randint(5000, 13000)
    status = "OK" if steps >= 8000 else "low"
    print(f"\n{day}: {steps} steps ({status})")

#The datetime module
from datetime import datetime, date

#Todays date and time
now = datetime.now()
print("\nCurrent datetime:", now)

#Just the date
today = date.today()
print("Today:", today)
print("Year:", today.year)
print("Month:", today.month)
print("Day:", today.day)

#Days between two dates
start = date(2025, 1, 1)
end = date(2025, 12, 31)
delta = end - start
print("Days in 2025: ", delta.days)

from datetime import date

#How many days until a goal date?
today = date.today()
goal_date = date(2025, 12, 31)
days_left = (goal_date - today).days
print(f"\nDays until end of 2025: {days_left}")

#format the date as text
formatted = today.strftime("%d %B %Y")
print("Today's date:", formatted)

#Importing specific functions - You can import specific functions that you want to use without have to call the whole module.
from math import sqrt, floor, ceil
from random import randint, choice

#No need to write math.sqrt() or random.randint()
print("\nSquare root of 225:", sqrt(225))
print("\nFloor of 9.7:", floor(9.7))

protocols = ["OMAD", "2MAD", "Autophagy Marathon"]
print("\nToday's protocol:", choice(protocols))
print("\nRandom step bonus:", randint(100, 500), "steps")