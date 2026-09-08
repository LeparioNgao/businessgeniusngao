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