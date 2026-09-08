#Write a function called weekly_report(name, steps_list, goal=8000) that takes a name, a list of step counts, and an optional goal. The function should calculate how many days hit the goal and print a summary including the name, total days, days on target, and average steps. Test it with two different names and step lists.
def weekly_report(name, steps_list, goal=8000):
    days_on_target = 0
    
    # 1. Calculate days hitting the goal
    for s in steps_list:
        if s >= goal:
            days_on_target += 1
            
    # 2. Calculate the average steps
    avg = sum(steps_list) / len(steps_list)
    
    # 3. Print the formatted summary
    print(f"--- {name}'s Week ---")
    print(f"Days tracked : {len(steps_list)}")
    print(f"Days on goal : {days_on_target}")
    print(f"Average steps: {round(avg, 0)}")
    print()

weekly_report("Lepario", [8500, 9000, 15000, 7600, 8600, 10000])
weekly_report("John", [9000, 8000, 12000, 7900, 15000, 6800, 10000])