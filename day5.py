daily_steps = [8200, 5100, 11300, 6800, 9400, 4200, 10100]
minimum_steps = 8000

#a for loop to iterate through the daily_steps list and check if each day's steps meet the minimum step goal
for steps in daily_steps:
    if steps >= minimum_steps:
        print(f"Excellent! You've met the daily step goal with {steps} steps!")
    else:
        print(f"You need to walk more to meet the daily step goal. You only walked {steps} steps.")

#a continue statement to skip any day below 5000 steps and calculate the weekly average steps
total_steps = 0
for steps in daily_steps:
    if steps < 5000:
        print(f"Skipping day with {steps} steps as it is below the minimum threshold.")
        continue
    total_steps += steps
average_steps = total_steps / len(daily_steps)
print(f"Your average steps for the week is: {average_steps}")

#a while loop to count how many consecutive days from the start hit the target before the first miss
consecutive_days = 0
i = 0
while i < len(daily_steps) and daily_steps[i] >= minimum_steps:
    consecutive_days += 1
    i += 1
print(f"You had {consecutive_days} consecutive days meeting the step goal.")