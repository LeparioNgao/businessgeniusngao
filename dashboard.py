#This is your Week 5 project.
# You will build a multi-section dashboard that pulls from three simulated API endpoints, processes the data, and outputs a complete report.
# Every concept from this week appears: nested JSON, key safety, processing functions, and structured output.

#What You Will Build
# 1. Fetch from three separate API endpoints (members, weekly logs, skill inventory)
# 2. Parse and process each endpoint's data independently
# 3. Combine all three into a single formatted dashboard output
# 4. Export the combined result as JSON

#Step 1: The Three Endpoints
#The dashboard calls three endpoints.
# In a script each would be a requests.get() call. Here each returns a hardcoded dict that mirrors an API response exactly.

#Endpoint 1
#GET /v1/members?city=Nairobi: returns a list of members with their today stats.

#Endpoint 2
#GET /v1/weekly-summary: returns aggregated step data for the past 7 days across all members.

#Endpoint 3
#GET /v1/skills/active: returns the list of active SMP skills being taught this week.

# Step 1: Preview all Endpoints

def fetch_members():
    return [
        {"name": "James Omondi",  "steps": 9200,  "protocol": "OMAD", "sleep": 7.5, "cold_shower": True},
        {"name": "Sandra Weru",   "steps": 10500, "protocol": "2MAD", "sleep": 8.0, "cold_shower": True},
        {"name": "Patrick Njiru", "steps": 8100,  "protocol": "OMAD", "sleep": 6.5, "cold_shower": False},
        {"name": "Grace Achieng", "steps": 11000, "protocol": "OMAD", "sleep": 7.0, "cold_shower": True},
        {"name": "Brian Kamau",   "steps": 7400,  "protocol": "2MAD", "sleep": 9.0, "cold_shower": True},
        {"name": "Kevin Mwangi",  "steps": 10800, "protocol": "OMAD", "sleep": 7.5, "cold_shower": True},
    ]

def fetch_weekly_summary():
    return {
        "week": "2024-W47",
        "daily_totals": [54200, 62000, 58400, 71000, 49600, 68000, 65200],
        "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "member_count": 6
    }

def fetch_active_skills():
    return {
        "week": "2024-W47",
        "skills": [
            {"name": "welding",       "instructor": "Patrick Njiru", "enrolled": 8},
            {"name": "tiling",        "instructor": "James Omondi",  "enrolled": 12},
            {"name": "copywriting",   "instructor": "Sandra Weru",   "enrolled": 15},
            {"name": "phone repair",  "instructor": "Kevin Mwangi",  "enrolled": 10},
            {"name": "beekeeping",    "instructor": "Grace Achieng", "enrolled": 6},
        ]
    }

# Preview
members = fetch_members()
weekly = fetch_weekly_summary()
skills = fetch_active_skills()

print(f"Members endpoint: {len(members)} records")
print(f"Weekly endpoint:  {len(weekly['daily_totals'])} days of data")
print(f"Skills endpoint:  {len(skills['skills'])} active skills")


#Step 2: Process Each Endpoint

def process_members(members, step_goal=10000):
    goal_met = [m for m in members if m["steps"] >= step_goal]
    avg_steps = round(sum(m["steps"] for m in members) / len(members))
    shower_count = sum(1 for m in members if m["cold_shower"])
    protocols = {}
    for m in members:
        p = m["protocol"]
        protocols[p] = protocols.get(p, 0) + 1
    return {
        "total": len(members),
        "goal_met": len(goal_met),
        "avg_steps": avg_steps,
        "cold_showers": shower_count,
        "protocols": protocols,
        "top": max(members, key=lambda m: m["steps"])["name"]
    }

def process_weekly(weekly):
    totals = weekly["daily_totals"]
    days = weekly["days"]
    best_idx = totals.index(max(totals))
    return {
        "best_day": days[best_idx],
        "best_total": max(totals),
        "weekly_avg": round(sum(totals) / len(totals)),
        "total_steps": sum(totals)
    }

def process_skills(skills_data):
    skills = skills_data["skills"]
    total_enrolled = sum(s["enrolled"] for s in skills)
    most_popular = max(skills, key=lambda s: s["enrolled"])
    return {
        "active_count": len(skills),
        "total_enrolled": total_enrolled,
        "most_popular": most_popular["name"],
        "top_enrollment": most_popular["enrolled"]
    }

# Run all three
raw_members = [
    {"name": "James Omondi",  "steps": 9200,  "protocol": "OMAD", "sleep": 7.5, "cold_shower": True},
    {"name": "Sandra Weru",   "steps": 10500, "protocol": "2MAD", "sleep": 8.0, "cold_shower": True},
    {"name": "Patrick Njiru", "steps": 8100,  "protocol": "OMAD", "sleep": 6.5, "cold_shower": False},
    {"name": "Grace Achieng", "steps": 11000, "protocol": "OMAD", "sleep": 7.0, "cold_shower": True},
    {"name": "Brian Kamau",   "steps": 7400,  "protocol": "2MAD", "sleep": 9.0, "cold_shower": True},
    {"name": "Kevin Mwangi",  "steps": 10800, "protocol": "OMAD", "sleep": 7.5, "cold_shower": True},
]
raw_weekly = {"week": "2024-W47", "daily_totals": [54200, 62000, 58400, 71000, 49600, 68000, 65200], "days": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], "member_count": 6}
raw_skills = {"week": "2024-W47", "skills": [{"name": "welding","instructor": "Patrick Njiru","enrolled": 8},{"name": "tiling","instructor": "James Omondi","enrolled": 12},{"name": "copywriting","instructor": "Sandra Weru","enrolled": 15},{"name": "phone repair","instructor": "Kevin Mwangi","enrolled": 10},{"name": "beekeeping","instructor": "Grace Achieng","enrolled": 6}]}

member_stats = process_members(raw_members)
weekly_stats = process_weekly(raw_weekly)
skill_stats = process_skills(raw_skills)

print("Member stats:", member_stats)
print("Weekly stats:", weekly_stats)
print("Skill stats: ", skill_stats)

#Step 3: Full Dashboard output

import json

# --- Data (simulated API responses) ---
raw_members = [
    {"name": "James Omondi",  "steps": 9200,  "protocol": "OMAD", "sleep": 7.5, "cold_shower": True},
    {"name": "Sandra Weru",   "steps": 10500, "protocol": "2MAD", "sleep": 8.0, "cold_shower": True},
    {"name": "Patrick Njiru", "steps": 8100,  "protocol": "OMAD", "sleep": 6.5, "cold_shower": False},
    {"name": "Grace Achieng", "steps": 11000, "protocol": "OMAD", "sleep": 7.0, "cold_shower": True},
    {"name": "Brian Kamau",   "steps": 7400,  "protocol": "2MAD", "sleep": 9.0, "cold_shower": True},
    {"name": "Kevin Mwangi",  "steps": 10800, "protocol": "OMAD", "sleep": 7.5, "cold_shower": True},
]
daily_steps = [54200, 62000, 58400, 71000, 49600, 68000, 65200]
day_names   = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
skills_list = [
    {"name": "welding",      "enrolled": 8},
    {"name": "tiling",       "enrolled": 12},
    {"name": "copywriting",  "enrolled": 15},
    {"name": "phone repair", "enrolled": 10},
    {"name": "beekeeping",   "enrolled": 6},
]

# --- Process ---
STEP_GOAL = 10000
goal_met = [m for m in raw_members if m["steps"] >= STEP_GOAL]
avg_steps = round(sum(m["steps"] for m in raw_members) / len(raw_members))
showers   = sum(1 for m in raw_members if m["cold_shower"])
best_day  = day_names[daily_steps.index(max(daily_steps))]
top_skill = max(skills_list, key=lambda s: s["enrolled"])

# --- Output ---
W = 52
print("=" * W)
print(f"  SMP COMMAND CENTRE DASHBOARD  |  Week 2024-W47")
print("=" * W)

print(f"\n  SECTION 1: MEMBER PERFORMANCE")
print(f"  {'Total members:':<28} {len(raw_members)}")
print(f"  {'Hit {STEP_GOAL:,} step goal:':}")
print(f"  Hit {STEP_GOAL:,} step goal:          {len(goal_met)}/{len(raw_members)}")
print(f"  {'Average steps:':<28} {avg_steps:,}")
print(f"  {'Cold showers today:':<28} {showers}/{len(raw_members)}")
print(f"  Goal hitters: {', '.join(m['name'] for m in goal_met)}")

print(f"\n  SECTION 2: WEEKLY STEPS")
for day, total in zip(day_names, daily_steps):
    bar = "#" * (total // 5000)
    print(f"  {day:4} {total:>7,}  {bar}")
print(f"  Best day: {best_day} ({max(daily_steps):,} total steps)")
print(f"  Week avg: {round(sum(daily_steps)/len(daily_steps)):,} steps/day")

print(f"\n  SECTION 3: ACTIVE SMP SKILLS")
for s in sorted(skills_list, key=lambda x: -x["enrolled"]):
    print(f"  {s['name']:15} {s['enrolled']} enrolled")
print(f"  Most popular: {top_skill['name']} ({top_skill['enrolled']} enrolled)")

print(f"\n{'=' * W}")

# JSON export
export = {
    "week": "2024-W47",
    "members": {"total": len(raw_members), "goal_met": len(goal_met), "avg_steps": avg_steps},
    "weekly": {"best_day": best_day, "total_steps": sum(daily_steps)},
    "skills": {"active": len(skills_list), "most_popular": top_skill["name"]}
}
print("\nJSON export:")
print(json.dumps(export, indent=2))

#Export to JSON

# Write to file
with open("dashboard_export.json", "w") as f:
    json.dump(export, f, indent=2)

print("Dashboard exported to dashboard_export.json")

#Post to an API

import requests
import json

# Send to an API endpoint
def send_to_api(data, api_url, api_key=None):
    headers = {
        "Content-Type": "application/json"
    }
    
    # If the API requires authentication
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    response = requests.post(api_url, json=data, headers=headers)
    
    if response.status_code == 201 or response.status_code == 200:
        print(f"✓ Success! Status: {response.status_code}")
        return response.json()
    else:
        print(f"✗ Error: {response.status_code} - {response.text}")
        return None

# Usage
 # JSONPlaceholder - a fake online REST API for testing
api_response = send_to_api(export, "https://jsonplaceholder.typicode.com/posts")

# Export to file (always works)
with open("dashboard_export.json", "w") as f:
    json.dump(export, f, indent=2)
print("✓ Exported to dashboard_export.json")

# Try API, but don't crash if it fails
try:
    api_response = send_to_api(export, "https://your-api-endpoint.com/reports")
except Exception as e:
    print(f"⚠ API unavailable: {e}")