#writing a week of discipline logs as text lines, then read them back and count how many days recorded 8,000 or more steps. Use the split and strip techniques from this lesson to parse each line.
weekly_data = """Monday: 8200
Tuesday: 14500
Wednesday: 10500
Thursday: 5500
Friday: 15000
Saturday: 7650
Sunday: 9600
"""
goal = 8000
days_on_goal = 0

for line in weekly_data.strip().split("\n"):
    line = line.strip()
    if ":" in line:
        day, steps_str = line.split(":", 1)
        steps = int(steps_str.strip())
        if steps >= goal:
            days_on_goal += 1
            print(f"{day}: {steps} steps - Goal hit")
        else:
            print(f"{day}: {steps} steps - Below goal")

print(f"\nTotal days on goal: {days_on_goal}")