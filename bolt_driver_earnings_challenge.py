data = {
    "driver": "Kamau Njoroge",
    "date": "2026-08-13",
    "trips": [
        {"route": "Westlands to CBD",     "fare_kes": 560},
        {"route": "CBD to South B",       "fare_kes": 420},
        {"route": "South B to Karen",     "fare_kes": 980},
        {"route": "Karen to Westlands",   "fare_kes": 720},
        {"route": "Westlands to Airport", "fare_kes": 740},
    ]
}

# Count trips
total_trips = len(data["trips"])

# Calculate total earnings
total_earned = sum(trip["fare_kes"] for trip in data["trips"])

# Find highest-paying trip
highest_trip = max(data["trips"], key=lambda trip: trip["fare_kes"])

# Print results
print(f"Total trips: {total_trips}")
print(f"Total earned: KES {total_earned}")
print(f"Highest trip: {highest_trip['route']} | KES {highest_trip['fare_kes']}")
