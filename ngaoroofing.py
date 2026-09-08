# Ngao Roofing job tracker.

# Roofing contractor job records
jobs = [
    {"client": "Kamau", "location": "Kiambu", "tile_type": "Shingle", "sheets_used": 500, "price_per_sheet": 1500},
    {"client": "Mutua", "location": "Machakos", "tile_type": "Classic", "sheets_used": 150, "price_per_sheet": 1500},
    {"client": "Odhiambo", "location": "Kisumu", "tile_type": "Romano", "sheets_used": 1500, "price_per_sheet": 1500},
    {"client": "Wanjiru", "location": "Nakuru", "tile_type": "Thatch", "sheets_used": 4500, "price_per_sheet": 1500},
]

print("Roofing Job Summary:")
print("-" * 50)
total_sheets = 0
total_revenue = 0

for job in jobs:
    revenue = job["sheets_used"] * job["price_per_sheet"]
    print(        f"{job['client']} ({job['location']}, {job['tile_type']}): "
        f"{job['sheets_used']} sheets | KES {revenue:,}"
    )
    total_sheets += job["sheets_used"]
    total_revenue += revenue

average_price = total_revenue / total_sheets

print(f"\nTotal sheets installed: {total_sheets}")
print(f"Total revenue: KES {total_revenue:,}")
print(f"Average price per sheet: KES {average_price:.0f}")


