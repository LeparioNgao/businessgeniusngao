weekly_steps = [10000, 12000, 8000, 7250, 11000, 7800, 13000]
for steps in weekly_steps:
   if steps >= 8000:
      print(steps , "Goal Hit")
   else:
        print(steps , "Below Goal")

print("Days tracked:", len(weekly_steps))

#You can also change items in a list
print("Before:", weekly_steps)

#update weekly_steps to add 15000 steps for the last day
weekly_steps[6] = 15000
print("After:", weekly_steps)

#Checking if a value is in a list
skills_learned = ["Python", "Java", "C++", "JavaScript"]
if "Python" in skills_learned:
    print("Python is in the list of skills learned.")
if "Ruby" not in skills_learned:
    print("Ruby is not in the list of skills learned.")

#add a new skill to the list
skills_learned.append("Ruby")
print("Updated skills learned:", skills_learned)