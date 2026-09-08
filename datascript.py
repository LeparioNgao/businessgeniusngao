#Individual API calls are the building block.
# A production script is a structure: configuration, fetch functions, processing functions, and output, all wired together cleanly.
# This lesson shows you how to organize API code so it is readable, reusable, and easy to extend.

#Learning Objectives
# 1. Understand the four-part structure of a production API script
# 2. Write a fetch function that handles errors and returns clean data
# 3. Write a processing function that transforms raw data
# 4. Combine configuration, fetching, processing, and output into one script
# 5. Save API results to a JSON file

#The Four Parts of a Production API Script.
#A well-organized API script has four parts:
# Configuration holds all settings (URL, keys, parameters) in one place.
# Fetch makes the HTTP request and handles errors.
# Process transforms raw data into what you need.
# Output prints, saves, or sends the results.

#Keeping these four stages separate makes the script easier to debug. When something breaks, you know immediately which stage to look at.

#Part 1: Configuration.
#Put all settings at the top of the script. Do not scatter URL strings and limit values throughout your code.
# When something needs to change, you change it in one place.

import os

# Configuration
BASE_URL = "https://api.smptracker.com/v1"
API_KEY = os.environ.get("SMP_API_KEY", "demo_key_123")
DEFAULT_CITY = "Nairobi"
STEP_GOAL = 10000
MAX_RESULTS = 50

print("Configuration loaded:")
print(f"  Base URL:   {BASE_URL}")
print(f"  API Key:    {API_KEY[:8]}...")
print(f"  City:       {DEFAULT_CITY}")
print(f"  Step Goal:  {STEP_GOAL:,}")
print(f"  Max Results:{MAX_RESULTS}")

#Part 2: Fetching Data.
#The fetch function makes the API call and returns clean data or raises an exception. It does not process, print, or save. It only fetches. Keep it focused.

# Simulates what a fetch function does in a script

def fetch_members(city="Nairobi", limit=50):
    """
    Fetches member data from the SMP API.
    Returns a list of member dicts or raises RuntimeError.
    In production: uses requests.get() with headers and params.
    """
    # Simulate the API response
    mock_response_status = 200
    mock_data = [
        {"id": 1, "name": "James Omondi",  "city": "Nairobi",  "steps": 9200,  "protocol": "OMAD"},
        {"id": 2, "name": "Sandra Weru",   "city": "Nairobi",  "steps": 10500, "protocol": "2MAD"},
        {"id": 3, "name": "Patrick Njiru", "city": "Mombasa",  "steps": 8100,  "protocol": "OMAD"},
        {"id": 4, "name": "Grace Achieng", "city": "Nairobi",  "steps": 11000, "protocol": "OMAD"},
        {"id": 5, "name": "Brian Kamau",   "city": "Kisumu",   "steps": 7400,  "protocol": "2MAD"},
        {"id": 6, "name": "Kevin Mwangi",  "city": "Nairobi",  "steps": 10800, "protocol": "OMAD"},
    ]

    if mock_response_status != 200:
        raise RuntimeError(f"API error: status {mock_response_status}")

    # Filter by city
    filtered = [m for m in mock_data if m["city"] == city]
    return filtered[:limit]


# Call the function
members = fetch_members(city="Nairobi")
print(f"\nFetched {len(members)} members from Nairobi")
for m in members:
    print(f"\n{m['name']}: {m['steps']} steps")

#Part 3: Processing Function
#The processing function takes raw data and returns something useful: computed stats, filtered records, or a restructured format. It does not fetch or print.

def process_members(members, step_goal=10000):
    """
    Takes a list of raw member records.
    Returns a summary dict with stats and categorized members.
    """
    if not members:
        return {"error": "No members to process"}

    total = len(members)
    goal_met = [m for m in members if m["steps"] >= step_goal]
    goal_missed = [m for m in members if m["steps"] < step_goal]
    avg_steps = round(sum(m["steps"] for m in members) / total)
    top_performer = max(members, key=lambda m: m["steps"])

    return {
        "total_members": total,
        "goal_met_count": len(goal_met),
        "goal_missed_count": len(goal_missed),
        "average_steps": avg_steps,
        "top_performer": top_performer["name"],
        "top_steps": top_performer["steps"],
        "goal_met": [m["name"] for m in goal_met],
    }


# Test with sample data
raw_members = [
    {"name": "James Omondi",  "steps": 9200,  "protocol": "OMAD"},
    {"name": "Sandra Weru",   "steps": 10500, "protocol": "2MAD"},
    {"name": "Grace Achieng", "steps": 11000, "protocol": "OMAD"},
    {"name": "Brian Kamau",   "steps": 7400,  "protocol": "2MAD"},
    {"name": "Kevin Mwangi",  "steps": 10800, "protocol": "OMAD"},
]

summary = process_members(raw_members, step_goal=10000)
print("\nProcessed summary:")
for key, value in summary.items():
    print(f"  \n{key}: {value}")

#Part 4: Output.
#The output stage prints the report, saves it to a file, or sends it somewhere. Here it does both: prints a formatted report and saves results as JSON.

import json

def print_report(summary, city="Mombasa"):
    print("=" * 48)
    print(f"  SMP MEMBER REPORT: {city.upper()}")
    print("=" * 48)
    print(f"  Total members:    {summary['total_members']}")
    print(f"  Hit step goal:    {summary['goal_met_count']}")
    print(f"  Missed goal:      {summary['goal_missed_count']}")
    print(f"  Average steps:    {summary['average_steps']:,}")
    print(f"  Top performer:    {summary['top_performer']} ({summary['top_steps']:,} steps)")
    print("-" * 48)
    print("  Members who hit goal:")
    for name in summary["goal_met"]:
        print(f"    {name}")
    print("=" * 48)


summary = {
    "total_members": 5,
    "goal_met_count": 3,
    "goal_missed_count": 2,
    "average_steps": 9780,
    "top_performer": "Grace Achieng",
    "top_steps": 11000,
    "goal_met": ["Sandra Weru", "Grace Achieng", "Kevin Mwangi"]
}

print_report(summary, city="Nairobi")

# Save to JSON
output = json.dumps(summary, indent=2)
print("\nJSON output saved:")
print(output)

#Export to JSON file:
with open("member_report.json", "w") as f:
    json.dump(summary, f)


#Putting it all together, the script has a clear structure: configuration, fetching, processing, and output. Each part is focused on one task, making it easy to read, debug, and extend.

import json
import os

# --- Configuration ---
BASE_URL = "https://api.smptracker.com/v1"
API_KEY = os.environ.get("SMP_API_KEY", "demo_key_123")
TARGET_CITY = "Mombasa"
STEP_GOAL = 10000

# --- Fetch ---
def fetch_members(city, limit=50):
    # Simulated API response
    all_members = [
        {"name": "James Omondi",  "city": "Nairobi",  "steps": 9200,  "protocol": "OMAD", "sleep": 7.5},
        {"name": "Sandra Weru",   "city": "Nairobi",  "steps": 10500, "protocol": "2MAD", "sleep": 8.0},
        {"name": "Patrick Njiru", "city": "Mombasa",  "steps": 8100,  "protocol": "OMAD", "sleep": 6.5},
        {"name": "Grace Achieng", "city": "Nairobi",  "steps": 11000, "protocol": "OMAD", "sleep": 7.0},
        {"name": "Brian Kamau",   "city": "Kisumu",   "steps": 7400,  "protocol": "2MAD", "sleep": 9.0},
        {"name": "Kevin Mwangi",  "city": "Nairobi",  "steps": 10800, "protocol": "OMAD", "sleep": 7.5},
        {"name": "Aisha Abdi",    "city": "Mombasa",  "steps": 12000, "protocol": "OMAD", "sleep": 8.0},
    ]
    return [m for m in all_members if m["city"] == city][:limit]

# --- Process ---
def process_members(members, step_goal):
    goal_met = [m for m in members if m["steps"] >= step_goal]
    avg_steps = round(sum(m["steps"] for m in members) / len(members)) if members else 0
    avg_sleep = round(sum(m["sleep"] for m in members) / len(members), 1) if members else 0
    top = max(members, key=lambda m: m["steps"]) if members else {}
    return {
        "total": len(members),
        "goal_met": len(goal_met),
        "avg_steps": avg_steps,
        "avg_sleep": avg_sleep,
        "top_name": top.get("name", "N/A"),
        "top_steps": top.get("steps", 0),
        "achievers": [m["name"] for m in goal_met]
    }

# --- Output ---
def print_report(city, summary):
    print(f"\n{'='*48}")
    print(f"  SMP DAILY REPORT: {city.upper()}")
    print(f"{'='*48}")
    print(f"  Members:       {summary['total']}")
    print(f"  Hit {STEP_GOAL:,} steps: {summary['goal_met']}")
    print(f"  Avg steps:     {summary['avg_steps']:,}")
    print(f"  Avg sleep:     {summary['avg_sleep']} hrs")
    print(f"  Top:           {summary['top_name']} ({summary['top_steps']:,})")
    print(f"\n  Achievers: {', '.join(summary['achievers'])}")
    print(f"{'='*48}\n")

# --- Main ---
members = fetch_members(TARGET_CITY)
summary = process_members(members, STEP_GOAL)
print_report(TARGET_CITY, summary)
import json
import os

# --- Configuration ---
BASE_URL = "https://api.smptracker.com/v1"
API_KEY = os.environ.get("SMP_API_KEY", "demo_key_123")
TARGET_CITY = "Mombasa"
STEP_GOAL = 10000

# --- Fetch ---
def fetch_members(city, limit=50):
    # Simulated API response
    all_members = [
        {"name": "James Omondi",  "city": "Nairobi",  "steps": 9200,  "protocol": "OMAD", "sleep": 7.5},
        {"name": "Sandra Weru",   "city": "Nairobi",  "steps": 10500, "protocol": "2MAD", "sleep": 8.0},
        {"name": "Patrick Njiru", "city": "Mombasa",  "steps": 8100,  "protocol": "OMAD", "sleep": 6.5},
        {"name": "Grace Achieng", "city": "Nairobi",  "steps": 11000, "protocol": "OMAD", "sleep": 7.0},
        {"name": "Brian Kamau",   "city": "Kisumu",   "steps": 7400,  "protocol": "2MAD", "sleep": 9.0},
        {"name": "Kevin Mwangi",  "city": "Nairobi",  "steps": 10800, "protocol": "OMAD", "sleep": 7.5},
        {"name": "Aisha Abdi",    "city": "Mombasa",  "steps": 12000, "protocol": "OMAD", "sleep": 8.0},
    ]
    return [m for m in all_members if m["city"] == city][:limit]

# --- Process ---
def process_members(members, step_goal):
    goal_met = [m for m in members if m["steps"] >= step_goal]
    avg_steps = round(sum(m["steps"] for m in members) / len(members)) if members else 0
    avg_sleep = round(sum(m["sleep"] for m in members) / len(members), 1) if members else 0
    top = max(members, key=lambda m: m["steps"]) if members else {}
    return {
        "total": len(members),
        "goal_met": len(goal_met),
        "avg_steps": avg_steps,
        "avg_sleep": avg_sleep,
        "top_name": top.get("name", "N/A"),
        "top_steps": top.get("steps", 0),
        "achievers": [m["name"] for m in goal_met]
    }

# --- Output ---
def print_report(city, summary):
    print(f"\n{'='*48}")
    print(f"  SMP DAILY REPORT: {city.upper()}")
    print(f"{'='*48}")
    print(f"  Members:       {summary['total']}")
    print(f"  Hit {STEP_GOAL:,} steps: {summary['goal_met']}")
    print(f"  Avg steps:     {summary['avg_steps']:,}")
    print(f"  Avg sleep:     {summary['avg_sleep']} hrs")
    print(f"  Top:           {summary['top_name']} ({summary['top_steps']:,})")
    print(f"\n  Achievers: {', '.join(summary['achievers'])}")
    print(f"{'='*48}\n")

# --- Main ---
members = fetch_members(TARGET_CITY)
summary = process_members(members, STEP_GOAL)
print_report(TARGET_CITY, summary)