steps = [8800, 6500, 11000, 9200, 7300]
steps.append(10500)  # Adding a new step count to the list
steps.remove(6500)  # Removing a specific step count from the list
steps.sort(reverse= True)  # Sorting the list in descending order
print("Final list:", steps)

#Count days that exceeded 9000 steps
exceeded_days = 0
for step in steps:
    if step > 9000:
        exceeded_days += 1
print("Number of days that exceeded 9000 steps:", exceeded_days)