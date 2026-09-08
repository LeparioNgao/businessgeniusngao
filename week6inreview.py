# Dataframes.

import pandas as pd
# Create a DataFrame from a dictionary and inspect it
data = {
    "name": ["Eric", "James", "Amina", "Sara"],
    "score": [85, 72, 91, 68],
    "city": ["Nairobi", "Mombasa", "Nairobi", "Kisumu"]
}
df = pd.DataFrame(data)
print(df)
print("\nShape:", df.shape)

# Filtering.

import pandas as pd
data = {"name": ["Eric","James","Amina","Sara"], "score": [85,72,91,68], "city": ["Nairobi","Mombasa","Nairobi","Kisumu"]}
df = pd.DataFrame(data)
# Filter to show only students from Nairobi with score above 80
result = df[(df['city'] == 'Nairobi') & (df['score'] > 80)]
result = df[df['score'] > 70]
print(result)

# Grouping

import pandas as pd
data = {"name": ["Eric","James","Amina","Sara"], "score": [85,72,91,68], "city": ["Nairobi","Mombasa","Nairobi","Kisumu"]}
df = pd.DataFrame(data)
# Group by city and get the average score per city
print(df.groupby('city')['score'].mean())

# NUMPY CHALLENGE

import numpy as np
# Create an array of 10 random integers between 1 and 100
# Print the mean, max, min, and standard deviation
arr = np.array([23, 67, 45, 89, 12, 56, 78, 34, 90, 41])
print(f"Mean: {arr.mean():.2f}")
print(f"Max: {arr.max()}")
print(f"Min: {arr.min()}")
print(f"Std: {arr.std():.2f}")

# Trade Application - Tiling Contractor Job Tracker.

#A tiling contractor tracks jobs completed across different clients. 
#Calculate total boxes laid, total revenue, and the average price per box across all jobs.
# Add your own job and re-run.

# Tiling contractor job records
jobs = [
    {"client": "Kamau", "location": "Kiambu", "boxes_used": 30, "price_per_box": 1800},
    {"client": "Mutua", "location": "Machakos", "boxes_used": 48, "price_per_box": 2100},
    {"client": "Odhiambo", "location": "Kisumu", "boxes_used": 20, "price_per_box": 1600},
    {"client": "Wanjiru", "location": "Nakuru", "boxes_used": 60, "price_per_box": 2200},
]

print("Job Summary:")
print("-" * 50)
total_boxes = 0
total_revenue = 0

for j in jobs:
    revenue = j["boxes_used"] * j["price_per_box"]
    print(f"{j['client']} ({j['location']}): {j['boxes_used']} boxes | KES {revenue:,}")
    total_boxes += j["boxes_used"]
    total_revenue += revenue

avg_price = total_revenue / total_boxes

print(f"\nTotal boxes laid: {total_boxes}")
print(f"Total revenue: KES {total_revenue:,}")
print(f"Average price per box: KES {avg_price:.0f}")

# Weekly milk yield per cow (litres)

herd_data = [
    {"cow": "Daisy", "yields": [72, 68, 74, 70]},
    {"cow": "Bella", "yields": [45, 42, 38, 40]},
    {"cow": "Nala",  "yields": [88, 91, 85, 93]},
    {"cow": "Rosa",  "yields": [55, 58, 52, 50]},
    {"cow": "Lola",  "yields": [78, 80, 76, 82]},
]

MINIMUM_WEEKLY = 60
top_cow = None
top_total = 0

print(f"{'Cow':<8} {'Total':>8} {'Avg/wk':>8} {'Status':>10}")
print("-" * 38)

for cow in herd_data:
    total = sum(cow["yields"])
    avg = total / len(cow["yields"])
    status = "OK" if avg >= MINIMUM_WEEKLY else "NEEDS ATTENTION"
    print(f"{cow['cow']:<8} {total:>8} {avg:>8.1f} {status:>10}")
    if total > top_total:
        top_total = total
        top_cow = cow["cow"]

print(f"\nTop producer: {top_cow} ({top_total} litres over 4 weeks)")