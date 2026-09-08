#Pandas is built on top of NumPy.
# scikit-learn uses NumPy arrays as its primary data format.
# TensorFlow and PyTorch are built on the same concept.
# Understanding NumPy is understanding the foundation of all numerical computing in Python.

#Learning Objectives
# 1. Understand what a NumPy array is and how it differs from a Python list
# 2. Create arrays using np.array(), np.zeros(), np.ones(), and np.arange()
# 3. Apply vectorized operations without loops
# 4. Use statistical functions: mean, std, min, max, percentile
# 5. Slice and filter arrays
# 6. Understand how NumPy and pandas work together

# 1. What is a NumPy array?
#A NumPy array is a fixed-type, fixed-size sequence of numbers stored in a single block of memory.
# Unlike a Python list, every element must be the same type (all integers, or all floats).
# This constraint is what makes NumPy arrays 10 to 100 times faster than lists for numerical operations.
#NumPy trades flexibility for raw numerical speed.

# 2. Creating arrays.

import numpy as np

# From a Python list
steps = np.array([9200, 10500, 8800, 11000, 7600, 9400, 10200])
print("steps array:", steps)
print("type:", type(steps))
print("dtype:", steps.dtype)
print("shape:", steps.shape)

# Zeros and ones
print("\nnp.zeros(5):", np.zeros(5))
print("np.ones(5):", np.ones(5))

# Range of numbers
print("np.arange(1, 8):", np.arange(1, 8))

# Evenly spaced
print("np.linspace(0, 1, 5):", np.linspace(0, 1, 5))

# 3. Vectoried Operations.

import numpy as np

steps = np.array([9200, 10500, 8800, 11000, 7600, 9400, 10200])
goal  = 10000

# All at once, no loop needed
deficit = steps - goal
print("\nSteps vs 10k goal:", deficit)

# Percentage of goal achieved
pct = (steps / goal * 100).round(1)
print("\nPercent of goal:", pct)

# Boolean mask: which days hit the goal?
hit = steps >= goal
print("\nHit goal:", hit)
print("\nDays hitting goal:", steps[hit])

#Using a boolean array inside brackets filters the array. steps[steps >= goal] returns only the values where the condition is True.
# No loop, no list comprehension needed.
print(steps[steps >= goal])


# 4. Statistical Functions

#Function	                 What It Computes
#np.mean(arr)	              Average value
#np.median(arr)	              Middle value when sorted
#np.std(arr)	              Standard deviation
#np.min(arr)	              Smallest value
#np.max(arr)	              Largest value
#np.sum(arr)	              Total of all values
#np.percentile(arr, 75)	      75th percentile value

import numpy as np

# 4 weeks of daily steps (28 days)
steps_28 = np.array([
    9200, 10500, 8800, 11000, 7600, 9400, 10200,
    8900, 10800, 9100, 11200, 7900, 10000, 9700,
    9500, 10300, 8600, 11500, 8200, 9800, 10600,
    9000, 10100, 8400, 10900, 7500, 9600, 10400
])

print(f"\n28-day step analysis")
print(f"  \nMean:        {np.mean(steps_28):,.0f}")
print(f"  \nMedian:      {np.median(steps_28):,.0f}")
print(f"  \nStd dev:     {np.std(steps_28):,.0f}")
print(f"  \nMin:         {np.min(steps_28):,}")
print(f"  \nMax:         {np.max(steps_28):,}")
print(f"  \nTotal:       {np.sum(steps_28):,}")
print(f"  \n75th pctile: {np.percentile(steps_28, 75):,.0f}")
print(f"  \nDays 10k+:   {np.sum(steps_28 >= 10000)}/28")

# 5. Array Slicing
#Slicing NumPy arrays uses the same syntax as Python lists.
# The difference is that slices of NumPy arrays are views, not copies. Changing a slice changes the original.

import numpy as np

steps = np.array([9200, 10500, 8800, 11000, 7600, 9400, 10200])
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

print("\nFirst 3 days:", steps[:3])
print("\nLast 2 days:", steps[-2:])
print("\nWeekdays (Mon-Fri):", steps[:5])
print("\nWeekend:", steps[5:])

print()
# Best week start: first day above 10k
first_10k = np.argmax(steps >= 10000)   # index of first True
print(f"\nFirst 10k+ day: {days[first_10k]} with {steps[first_10k]:,} steps")

# Sort and show progression
sorted_steps = np.sort(steps)
print("\nSteps sorted low to high:", sorted_steps)

# 6. NumPy and Pandas Together.
#NumPy and pandas work together.
# A pandas Series is built on a NumPy array.
# You can pull a column out of a DataFrame as a NumPy array using .values or .to_numpy().
# Many pandas methods internally use NumPy for speed

import pandas as pd
import numpy as np

df = pd.DataFrame({
    "day":      ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "steps":    [9900, 10900, 9800, 14000, 8600, 7400, 8200],
    "bench_press_kg": [80, 82, 78, 85, 80, 83, 84],
    "sleep_hr": [7.5, 8.0, 6.5, 7.0, 9.0, 7.5, 8.0],
})

# Pull a column as a NumPy array
steps_arr = df["steps"].to_numpy()
bench_arr = df["bench_press_kg"].to_numpy()
print("\nNumPy array from pandas column:", steps_arr)
print("\nType:", type(steps_arr))
print("\nSteps and bench press correlation:")
print(np.corrcoef(steps_arr, bench_arr))

# Use NumPy on it
print(f"\nMean:    {np.mean(steps_arr):,.0f}")
print(f"Std dev: {np.std(steps_arr):,.0f}")

# Add a normalized column back to the DataFrame
# Normalize to 0-1 range (min-max scaling)
df["steps_norm"] = (df["steps"] - df["steps"].min()) / (df["steps"].max() - df["steps"].min())
df["steps_norm"] = df["steps_norm"].round(3)
print("\nWith normalized steps:")
print(df[["day", "steps", "bench_press_kg", "steps_norm"]].to_string())