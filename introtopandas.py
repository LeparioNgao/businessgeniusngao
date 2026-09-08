#Lists and dictionaries work for dozens of records.
# When you have hundreds or thousands of rows, you need a tool built for structured data.
# Pandas is that tool. 
# It is the standard library for data analysis in Python, and it is what data analysts use every day.

#Learning Objectives
# 1. Understand what a DataFrame is and how it differs from a list
# 2. Create a DataFrame from a dictionary
# 3. Inspect a DataFrame with head(), shape, columns, and dtypes
# 4. Select single and multiple columns
# 5. Select rows using iloc and loc
# 6. Compute basic statistics with describe()

#When you work locally in VS Code, use pip in your terminal instead: pip install pandas.
# Run that once, then just import pandas as pd in your script. The import line is the same either way.

#What is a Data Frame?

#A DataFrame is a two-dimensional data structure with labeled rows and columns.
# Think of it as a Python spreadsheet. Each column is a Series (a labeled list).
# Each row is one record. You can filter, sort, group, compute, and reshape the whole table in a single line.

import pandas as pd

data = {
    "day":      ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "steps":    [9200, 10500, 8800, 11000, 7600, 9400, 10200],
    "sleep_hr": [7.5, 8.0, 6.5, 7.0, 9.0, 7.5, 8.0],
    "protocol": ["OMAD", "2MAD", "OMAD", "OMAD", "2MAD", "OMAD", "OMAD"],
    "cold_shower": [True, True, False, True, True, True, True]
}

df = pd.DataFrame(data)
print(df.to_string())

#Inspecting a Data Frame
#Before analyzing any dataset, inspect it. These four commands tell you what you are working with.

import pandas as pd

data = {
    "day":      ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "steps":    [9200, 10500, 8800, 11000, 7600, 9400, 10200],
    "sleep_hr": [7.5, 8.0, 6.5, 7.0, 9.0, 7.5, 8.0],
    "protocol": ["OMAD", "2MAD", "OMAD", "OMAD", "2MAD", "OMAD", "OMAD"],
    "cold_shower": [True, True, False, True, True, True, True]
}
df = pd.DataFrame(data)

print("\nShape (rows, cols):", df.shape)
print("\nColumns:", list(df.columns))
print("\nData types:")
print(df.dtypes)
print("\nFirst 3 rows:")
print(df.head(3).to_string())

#Selecting Columns
#Select one column with single brackets. Select multiple columns with a list inside double brackets.
# A single column returns a Series. Multiple columns return a DataFrame.

import pandas as pd

data = {
    "day":      ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "steps":    [9200, 10500, 8800, 11000, 7600, 9400, 10200],
    "sleep_hr": [7.5, 8.0, 6.5, 7.0, 9.0, 7.5, 8.0],
    "protocol": ["OMAD", "2MAD", "OMAD", "OMAD", "2MAD", "OMAD", "OMAD"],
}
df = pd.DataFrame(data)

# Single column (returns a Series)
print("\nSteps column:")
print(df["steps"])

print("\nSteps and protocol:")
print(df[["steps", "protocol"]].to_string())

#Selecting Rows
#.iloc selects rows by position (integer index). .loc selects rows by label. Both work like list slicing.

import pandas as pd

data = {
    "day":      ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "steps":    [9200, 10500, 8800, 11000, 7600, 9400, 10200],
    "sleep_hr": [7.5, 8.0, 6.5, 7.0, 9.0, 7.5, 8.0],
    "protocol": ["OMAD", "2MAD", "OMAD", "OMAD", "2MAD", "OMAD", "OMAD"],
}
df = pd.DataFrame(data)

# iloc: by position
print("\nFirst row (iloc[0]):")
print(df.iloc[0])

print("\nRows 0 to 2 (iloc[0:3]):")
print(df.iloc[0:3].to_string())

print("\nLast row (iloc[-1]):")
print(df.iloc[-1])

#loc: by label
print("\nFirst day (loc[0]):")
print(df.loc[0])

#Basic Statistics with describe()
#describe() gives you count, mean, std, min, max, and quartiles for every numeric column in one call.

import pandas as pd

data = {
    "day":      ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "steps":    [9200, 10500, 8800, 11000, 7600, 9400, 10200],
    "sleep_hr": [7.5, 8.0, 6.5, 7.0, 9.0, 7.5, 8.0],
    "water":    [7, 8, 6, 9, 8, 7, 8],
    "bench_press_kg": [80, 82, 78, 85, 80, 83, 84]
}
df = pd.DataFrame(data)

print("Statistics for all numeric columns:")
print(df.describe().to_string())

print("\nManual checks:")
print(f"Mean steps:  {df['steps'].mean():.0f}")
print(f"Max steps:   {df['steps'].max()}")
print(f"Min steps:   {df['steps'].min()}")
print(f"Total steps: {df['steps'].sum()}")
print(f"Bench Press Total: {df['bench_press_kg'].sum()}")

#Loading from a CSV
#In VS Code, loading a CSV file is one line. pd.read_csv() returns a DataFrame immediately.

# In VS Code

#import pandas as pd

#df = pd.read_csv("weekly_log.csv")
#print(df.head())
#print(df.shape)