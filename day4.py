#Creating a discipline grader

steps = 7500
sleep_hours = 6
water_glasses = 6
cold_shower = False
pages_read = 15

if steps >= 8000:
    print("Excellent! You've met the daily step goal!")
else:
    print("You need to walk more to meet the daily step goal.")
if sleep_hours >= 6:
    print("You've met the daily sleep goal!")
else:
    print("Your sleep goal has not been met.")
if water_glasses >= 6:
    print("You've met the daily water intake goal!")
else:
    print("You need to drink more water to meet the daily goal.")
if cold_shower:
    print("You've taken a cold shower today!")
else:
    print("You need to take a cold shower to meet the daily goal.")
if pages_read >= 20:
    print("You've met the daily reading goal!")
else:
    print("Your daily reading goal has not been met.")