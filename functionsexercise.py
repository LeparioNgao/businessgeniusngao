def day_report(steps, water, protocol):
    print("DAILY REPORT")
    print(f"Steps : {steps}")
    print(f"Water Glasses : {water}")
    print(f"Protocol : {protocol}")
    print()

def hit_goal(steps):
    return steps >= 8000

day_report(6500, 6, "2MAD")
day_report(9600, 8, "OMAD")
day_report(8000, 8, "Autophagy Marathon")

print("Goal hit(6500)?", hit_goal(6500))
print("Goal hit(9600)?", hit_goal(9600))
print("Goal hit(8000)", hit_goal(8000))