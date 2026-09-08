#Loading data is the first step.
# The next step is shaping it: keep only the rows you care about, create new columns from existing ones, rename and sort.
# These operations turn raw data into analysis-ready data.

#Learning Objectives
# 1. Filter rows using boolean conditions
# 2. Combine multiple conditions with & and |
# 3. Use .isin() to filter by a list of values
# 4. Add new computed columns
# 5. Rename and drop columns
# 6. Sort a DataFrame by one or more columns

# 1. Boolean Filtering.
#Boolean filtering selects rows where a condition is True.
# You write a condition that compares a column to a value.
# Pandas evaluates it for every row and returns only the matching ones. The result is a new DataFrame, not a modification of the original.

#Think of sorting tiles on a workbench.
#You have 100 tiles laid out. You pick up only the ones that are uncracked and 30x30cm.
# You do not change the tiles. You just choose which ones to work with.
# Boolean filtering works the same way: the original data stays untouched, and you get back only the rows that pass the condition.

import pandas as pd

df = pd.DataFrame({
    "day":      ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "steps":    [9200, 10500, 8800, 11000, 7600, 9400, 10200],
    "sleep_hr": [7.5, 8.0, 6.5, 7.0, 9.0, 7.5, 8.0],
    "water_glasses": [7, 8, 6, 9, 8, 7, 8],
    "protocol": ["OMAD", "2MAD", "OMAD", "OMAD", "2MAD", "OMAD", "OMAD"],
})

# Days where step goal was hit
goal_days = df[df["steps"] >= 10000]
print("Days with 10k+ steps:")
print(goal_days[["day", "steps", "protocol"]].to_string())

print()
# Days with less than 7.5 hours sleep
low_sleep = df[df["sleep_hr"] < 7.5]
print("Days with under 7.5 hours sleep:")
print(low_sleep[["day", "sleep_hr"]].to_string())

# 2. Multiple Conditions.
#Combine conditions with & (AND) and | (OR). Each condition must be wrapped in parentheses.

# OMAD days with 10k+ steps
omad_goal = df[(df["protocol"] == "OMAD") & (df["steps"] >= 10000)]
print("OMAD days with 10k+ steps:")
print(omad_goal[["day", "steps", "protocol"]].to_string())

print()
# Days with either goal steps OR 8+ hours sleep
either = df[(df["steps"] >= 10000) | (df["sleep_hr"] >= 8.0)]
print("Days with 10k+ steps OR 8+ hrs sleep:")
print(either[["day", "steps", "sleep_hr"]].to_string())

#Use & for AND, | for OR. Do not use Python's and and or keywords in pandas conditions. They do not work on Series and will raise an error.

# 3. Filtering with .isin()
#.isin() checks if a column's value is in a list. It is cleaner than chaining multiple | conditions when you have several allowed values.

df = pd.DataFrame({
    "name":     ["James Omondi", "Sandra Weru", "Patrick Njiru", "Grace Achieng", "Brian Kamau", "Kevin Mwangi"],
    "city":     ["Nairobi", "Mombasa", "Nairobi", "Kisumu", "Nairobi", "Mombasa"],
    "steps":    [9200, 10500, 8100, 11000, 7400, 10800],
    "protocol": ["OMAD", "2MAD", "OMAD", "OMAD", "2MAD", "OMAD"],
})

# Members from Nairobi or Mombasa
nbi_msa = df[df["city"].isin(["Nairobi", "Mombasa"])]
print("Nairobi and Mombasa members:")
print(nbi_msa[["name", "city", "steps"]].to_string())

# 4. Adding New Columns
#Add a new column by assigning to a column name that does not exist yet. The right side can be a calculation using existing columns.

import pandas as pd

df = pd.DataFrame({
    "day":          ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "steps":        [9200, 10500, 8800, 11000, 7600, 9400, 10200],
    "sleep_hr":     [7.5, 8.0, 6.5, 7.0, 9.0, 7.5, 8.0],
    "water_glasses":[7, 8, 6, 9, 8, 7, 8],
    "protocol":     ["OMAD", "2MAD", "OMAD", "OMAD", "2MAD", "OMAD", "OMAD"],
})

# Boolean column: did we hit the step goal?
df["hit_goal"] = df["steps"] >= 10000

# Numeric column: steps deficit or surplus vs 10k goal
df["steps_vs_goal"] = df["steps"] - 10000

# Category column: water rating
df["hydration"] = df["water_glasses"].apply(lambda x: "Good" if x >= 8 else "Low")

print(df[["day", "steps", "hit_goal", "steps_vs_goal", "hydration"]].to_string())

# 5. Renaming and Dropping Columns.

import pandas as pd

df = pd.DataFrame({
    "day":      ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "steps":    [9200, 10500, 8800, 11000, 7600],
    "sleep_hr": [7.5, 8.0, 6.5, 7.0, 9.0],
    "protocol": ["OMAD", "2MAD", "OMAD", "OMAD", "2MAD"],
    "notes":    ["ok", "great", "tired", "best", "rest"],
})

# Rename column
df = df.rename(columns={"sleep_hr": "sleep_hours"})
print("After rename:")
print(list(df.columns))

# Drop a column
df = df.drop(columns=["notes"])
print("After drop:")
print(df.to_string())

# 6. Sorting
#sort_values() sorts by one or more columns. ascending=False sorts high to low.

import pandas as pd

df = pd.DataFrame({
    "name":     ["James Omondi", "Sandra Weru", "Patrick Njiru", "Grace Achieng", "Brian Kamau", "Kevin Mwangi"],
    "steps":    [9200, 10500, 8100, 11000, 7400, 10800],
    "sleep_hr": [7.5, 8.0, 6.5, 7.0, 9.0, 7.5],
})

# Sort by steps, highest first
ranked = df.sort_values("steps", ascending=False).reset_index(drop=True)
ranked.index = ranked.index + 1  # 1-based ranking

print("Step leaderboard:")
for i, row in ranked.iterrows():
    print(f"  #{i}  {row['name']:<20} {row['steps']:,} steps")

# Sort by sleep, highest first
sleep_ranked = df.sort_values("sleep_hr", ascending=False).reset_index(drop=True)
sleep_ranked.index = sleep_ranked.index + 1

print("Sleep leaderboard:")
for i, row in sleep_ranked.iterrows():
    print(f"  #{i}  {row['name']:<20} {row['sleep_hr']:.1f} hours")

most_sleep = sleep_ranked.iloc[0]
print(f"\nMost sleep: {most_sleep['name']} with {most_sleep['sleep_hr']:.1f} hours")

# Add wake_up_score
df["wake_up_score"] = df["sleep_hr"] * df["steps"] / 1000

# Sort by wake_up_score, highest first
score_ranked = df.sort_values("wake_up_score", ascending=False).reset_index(drop=True)
score_ranked.index = score_ranked.index + 1

print("\nWake-up score leaderboard:")
for i, row in score_ranked.iterrows():
    print(f"  #{i}  {row['name']:<20} {row['wake_up_score']:.2f}")