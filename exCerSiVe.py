#You have a simulated CSV of a week's step data. Read it with DictReader, convert steps to integers, filter out any days with steps below 7000 as invalid, and print the average steps for the valid days only.

import csv
import io

steps_data = """day,steps
Monday,9200
Tuesday,10500
Wednesday,5500
Thursday,11000
Friday,6800
Saturday,8000
Sunday,4000"""

f = io.StringIO(steps_data)
steps_reader = csv.DictReader(f)

valid_steps = []
for row in steps_reader:
    steps = int(row["steps"])
    if steps >= 7000:
        valid_steps.append(steps)
        print()
        print(f"{row['day']}: {steps} steps (valid)")
    else:
        print()
        print(f"{row['day']}: {steps} steps (invalid)")

if valid_steps:
    average_steps = sum(valid_steps) / len(valid_steps)
    print()
    print(f"Average steps for valid days: {average_steps}")


#Applied Example: Crop Harvest Tracker
#A crop farmer tracks harvest yield per field using a CSV. The same DictReader pattern reads each field's output and flags underperforming plots.

import csv, io

harvest_csv = """field,crop,bags_harvested,target_bags
North Plot,Maize,48,50
South Plot,Beans,22,30
East Plot,Wheat,61,55
West Plot,Maize,35,50
Centre Plot,Sorghum,44,40
"""

reader = csv.DictReader(io.StringIO(harvest_csv))

print(f"{'Field':<15} {'Crop':<10} {'Harvested':>10} {'Target':>8} {'Status':>12}")
print("-" * 58)

for row in reader:
    harvested = int(row["bags_harvested"])
    target = int(row["target_bags"])
    pct = (harvested / target) * 100
    status = "On target" if harvested >= target else f"Short by {target - harvested} bags"
    print(f"{row['field']:<15} {row['crop']:<10} {harvested:>10} {target:>8} {status:>12}")