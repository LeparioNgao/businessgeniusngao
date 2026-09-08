#Filtering shows you individual rows. Grouping shows you patterns across categories.
# "What is the average step count on OMAD days vs 2MAD days?"
# "Which city has the highest average bench press?"
# These are groupby questions. They are what turn raw data into insight.

#Learning Objectives
# 1. Understand what groupby does and when to use it
# 2. Aggregate with mean, sum, count, min, and max
# 3. Group by multiple columns
# 4. Use value_counts() to count unique values
# 5. Handle missing values (NaN) in a DataFrame

# 1. What is a Groupby?
#groupby splits a DataFrame into groups based on the values in one or more columns, then lets you apply a calculation to each group.
# The result is a summary table where each row represents one group. It answers questions like: "what is the average X for each category of Y?"

#Basic groupby

import pandas as pd

df = pd.DataFrame({
    "day":      ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "steps":    [9200, 10500, 8800, 11000, 7600, 9400, 10200],
    "sleep_hr": [7.5, 8.0, 6.5, 7.0, 9.0, 7.5, 8.0],
    "bench_press_kg": [80, 85, 78, 82, 88, 81, 84],
    "protocol": ["OMAD", "2MAD", "OMAD", "OMAD", "2MAD", "OMAD", "OMAD"],
})

# Average steps per fasting protocol
grouped = df.groupby("protocol")["steps"].mean().round(0)
print("Average steps by protocol:")
print(grouped)

print()
# Total steps per protocol
totals = df.groupby("protocol")["steps"].sum()
print("Total steps by protocol:")
print(totals)

# Average bench press per fasting protocol
bench_press_by_protocol = df.groupby("protocol")["bench_press_kg"].mean().round(1)
print("Average bench press by protocol (kg):")
print(bench_press_by_protocol)

# 2. Common Aggregation Functions.

import pandas as pd

df = pd.DataFrame({
    "name":     ["James", "Sandra", "Patrick", "Grace", "Brian", "Kevin", "James", "Sandra"],
    "city":     ["Nairobi", "Mombasa", "Nairobi", "Kisumu", "Nairobi", "Mombasa", "Nairobi", "Mombasa"],
    "steps":    [9200, 10500, 8100, 11000, 7400, 10800, 9800, 10200],
    "sleep_hr": [7.5, 8.0, 6.5, 7.0, 9.0, 7.5, 7.0, 8.5],
})

# Multiple aggregations on steps by city
city_stats = df.groupby("city")["steps"].agg(["mean", "max", "min", "count"]).round(0)
print("\nSteps statistics by city:")
print(city_stats)

# 3. Grouping multiple columns at once.

import pandas as pd

df = pd.DataFrame({
    "city":     ["Nairobi", "Nairobi", "Mombasa", "Mombasa", "Nairobi", "Kisumu", "Nairobi", "Kisumu", "Narok", "Narok"],
    "protocol": ["OMAD",    "2MAD",    "OMAD",    "2MAD",    "OMAD",    "OMAD",   "2MAD",    "2MAD",    "2MAD",   "2MAD"],
    "steps":    [9200, 10500, 8100, 11000, 9400, 10200, 7400, 8800, 15000, 7500],
    "sleep_hr": [7.5, 8.0, 6.5, 7.0, 7.5, 8.0, 9.0, 7.5, 8.0, 6.5],
})

# Average steps grouped by both city and protocol
breakdown = df.groupby(["city", "protocol"])["steps"].mean().round(0)
print("\nAverage steps by city and protocol:")
print(breakdown)

#value_counts()
#value_counts() counts how many times each unique value appears in a column. It returns a Series sorted by count, highest first.

import pandas as pd

df = pd.DataFrame({
    "name":     ["James", "Sandra", "Patrick", "Grace", "Brian", "Kevin", "James", "Grace", "Sandra", "James"],
    "protocol": ["OMAD", "2MAD", "OMAD", "OMAD", "2MAD", "OMAD", "OMAD", "OMAD", "2MAD", "OMAD"],
    "city":     ["Nairobi", "Mombasa", "Nairobi", "Kisumu", "Nairobi", "Mombasa", "Nairobi", "Kisumu", "Mombasa", "Nairobi"],
})

print("\nProtocol distribution:")
print(df["protocol"].value_counts())

print("\nCity distribution:")
print(df["city"].value_counts())

#Handling Missing Data
#Real data has gaps. Pandas represents missing values as NaN (Not a Number).
# Use isna() to find them, dropna() to remove rows with missing values, and fillna() to replace them with a default.

import pandas as pd

df = pd.DataFrame({
    "name":     ["James", "Sandra", "Patrick", "Grace", "Brian"],
    "steps":    [9200, None, 8100, 11000, None],
    "sleep_hr": [7.5, 8.0, None, 7.0, 9.0],
})

print("Original with NaN:")
print(df.to_string())

print("\nRows with any missing value:")
print(df[df.isna().any(axis=1)].to_string())

# Fill missing steps with the column mean
df["steps"] = df["steps"].fillna(df["steps"].mean())
df["sleep_hr"] = df["sleep_hr"].fillna(df["sleep_hr"].median())

print("\nAfter filling NaN:")
print(df.to_string())

#groupby splits data into categories and computes a metric per group.
# Chain it with .mean(), .sum(), .count(), or .agg() for multiple stats at once.
# value_counts() counts occurrences of each unique value.
# Handle missing data with isna(), fillna(), and dropna().
