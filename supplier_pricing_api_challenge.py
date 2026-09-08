data = {
    "supplier": "Nairobi Steel Ltd",
    "prices": {
        "mild_steel_sheet": 4500,
        "angle_iron": 2800
    }
}

# Calculate costs
mild_steel_cost = 3 * data["prices"]["mild_steel_sheet"]
angle_iron_cost = 6 * data["prices"]["angle_iron"]
total_cost = mild_steel_cost + angle_iron_cost

# Print results
print(f"Mild steel sheets (3): KES {mild_steel_cost}")
print(f"Angle iron (6m): KES {angle_iron_cost}")
print(f"Total: KES {total_cost}")
