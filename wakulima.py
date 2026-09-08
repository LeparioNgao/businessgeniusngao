import json

# Simulated crop market API response
response_text = '''
{
    "market": "Wakulima Market, Nairobi",
    "date": "2026-07-27",
    "prices_per_bag_kes": {
        "maize": 3800,
        "beans": 9200,
        "wheat": 5500,
        "sorghum": 3200
    },
    "bag_weight_kg": 90
}
'''

data = json.loads(response_text)

# Farmer's current stock in bags
stock = {"maize": 12, "beans": 5, "wheat": 8, "sorghum": 20}

print(f"Market: {data['market']}")
print(f"Date: {data['date']}\n")
print("Crop Valuation:")
print("-" * 40)

total_value = 0
for crop, bags in stock.items():
    price = data["prices_per_bag_kes"][crop]
    value = bags * price
    print(f"{crop.title()}: {bags} bags x KES {price:,} = KES {value:,}")
    total_value += value

print(f"\nTotal stock value: KES {total_value:,}")