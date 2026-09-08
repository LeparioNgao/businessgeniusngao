#A CSV file stores tabular data as plain text. Each line is one record. Values within a line are separated by commas. The first line typically contains column names (the header). Python's csv module reads this format and gives you rows as lists or dictionaries.
#A CSV file for a client list looks like this:

#name,phone,skill,city
#James Omondi,0712345678,welding,Nairobi
#Sandra Weru,0723456789,tiling,Mombasa
#Patrick Njiru,0734567890,phone repair,Nairobi

#csv.reader reads a CSV file and gives you each row as a list. The first row (the header) is just another list.

import csv
import io

# Simulated CSV content
csv_data = """name,phone,skill,city
James Omondi,0712345678,welding,Nairobi
Sandra Weru,0723456789,tiling,Mombasa
Patrick Njiru,0734567890,phone repair,Nairobi
Grace Achieng,0745678901,copywriting,Kisumu
Brian Kamau,0756789012,upholstery,Nairobi"""

f = io.StringIO(csv_data)
reader = csv.reader(f)

for row in reader:
    print()
    print(row)


#Each row is a Python list. The first row is the header. To skip it, call next(reader) before the loop.

import csv
import io

csv_data = """name,phone,skill,city
James Omondi,0712345678,welding,Nairobi
Sandra Weru,0723456789,tiling,Mombasa
Patrick Njiru,0734567890,phone repair,Nairobi"""

f = io.StringIO(csv_data)
reader = csv.reader(f)
next(reader)  # Skip header row

for row in reader:
    name, phone, skill, city = row
    print()
    print(f"{name} | {skill} | {city}")


#csv.DictReader automatically uses the first row as keys and gives you each row as a dictionary. This is the most practical way to read CSV data because you access values by column name, not by position.

import csv
import io

csv_datas = """name,steps,water,protocol,cold_shower
James Omondi,9200,8,OMAD,True
Sandra Weru,10500,9,2MAD,True
Patrick Njiru,7600,6,OMAD,False
Grace Achieng,11000,8,Autophagy Marathon,True"""

f = io.StringIO(csv_datas)
reader = csv.DictReader(f)

for row in reader:
    steps = int(row["steps"])
    status = "Goal hit" if steps >= 8000 else "Below goal"
    print()
    print(f"\n{row['name']}: {steps} steps | {row['protocol']} | {status}")

# All values from a CSV come in as strings. Convert them to the right type before using them in calculations. Use int() for whole numbers and float() for decimals.

#csv.writer writes rows to a CSV. Each call to writerow() writes one row as a list.

import csv
import io

output = io.StringIO()
writer = csv.writer(output)

# Write header
writer.writerow(["name", "steps", "protocol", "goal_hit"])

# Write data rows
data = [
    ["James",   9200,  "OMAD",              True],
    ["Sandra",  10500, "2MAD",              True],
    ["Patrick", 7600,  "OMAD",              False],
    ["Grace",   11000, "Autophagy Marathon", True],
]

for row in data:
    writer.writerow(row)

print()
print("Generated CSV:")
print(output.getvalue())

#csv.DictWriter writes dictionaries as CSV rows. You define the column names (fieldnames) upfront, then write each dictionary as a row.

import csv
import io

clients = [
    {"name": "James",   "skill": "welding",      "city": "Nairobi",  "sessions": 4},
    {"name": "Sandra",  "skill": "tiling",        "city": "Mombasa",  "sessions": 3},
    {"name": "Patrick", "skill": "phone repair",  "city": "Nairobi",  "sessions": 4},
    {"name": "Grace",   "skill": "copywriting",   "city": "Kisumu",   "sessions": 2},
]

output = io.StringIO()
fieldnames = ["name", "skill", "city", "sessions"]
writer = csv.DictWriter(output, fieldnames=fieldnames)

writer.writeheader()
writer.writerows(clients)

print()
print(output.getvalue())