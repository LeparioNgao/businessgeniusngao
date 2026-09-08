#Write a function called safe_log_entry(data) that takes a dictionary and tries to extract steps, water, and protocol. If steps is not a valid integer, print an error and return None. If water is missing, use a default of 0. If protocol is missing, use "Unknown". Print a clean report for each valid entry.

def safe_log_entry(data):
    try:
        steps = int(data.get("steps", 0))
        water = data.get("water", 0)
        protocol = data.get("protocol", "Unknown")
        print(f"Steps: {steps}, Water: {water}, Protocol: {protocol}")
        return {"steps": steps, "water": water, "protocol": protocol}
    except (ValueError, TypeError):
        print(f"Error: Invalid steps value. Skipping this entry.")
        return None

log_entries = [
    {"steps": "9200", "water": 2, "protocol": "OMAD"},
    {"steps": "not recorded", "water": 1, "protocol": "2MAD"},
    {"steps": "10500", "protocol": "Intermittent Fasting"},
    {"steps": None, "water": 3},
    {"steps": "8800", "water": 2, "protocol": "Unknown"},
]

results = [safe_log_entry(entry) for entry in log_entries]
valid_results = [result for result in results if result is not None]
print(f"Valid steps entries: {len(valid_results)}")
