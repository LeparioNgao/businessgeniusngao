fasting = "Autophagy Marathon"
cold_shower = True

# Write your if/elif/else logic below
print("=== DISCIPLINE CHECK ===")
print()

if fasting == "Autophagy Marathon":
    print("Fasting: 48-Hour Fast Active.")
elif fasting == "0MAD" or fasting == "2MAD":
    print("Fasting protocol active -", fasting)
else:
    print("Fasting: No protocol today.")

if fasting == "Autophagy Marathon" and cold_shower == True:
    print("Peak Discipline Day.")