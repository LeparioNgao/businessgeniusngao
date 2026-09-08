import pandas as pd

data = {
    "goat": ["Simba", "Kijana", "Mzee", "Damu", "Furaha", "Pendo", "Jasiri"],
    "breed": ["Boer", "Galla", "Boer", "Galla", "Boer", "Galla", "Boer"],
    "weight_kg": [28, 19, 35, 14, 32, 22, 17],
    "age_months": [18, 12, 36, 8, 24, 15, 10]
}

df = pd.DataFrame(data)

# Flag underweight: Boer target 25kg, Galla target 18kg
def weight_status(row):
    target = 25 if row["breed"] == "Boer" else 18
    return "OK" if row["weight_kg"] >= target else "Needs feeding"

df["status"] = df.apply(weight_status, axis=1)
df["weight_gap_kg"] = df.apply(
    lambda r: max(0, (25 if r["breed"] == "Boer" else 18) - r["weight_kg"]), axis=1
)

# Show underweight animals sorted by gap
priority = df[df["status"] == "Needs feeding"].sort_values("weight_gap_kg", ascending=False)
print("Priority feeding list:")
print(priority[["goat", "breed", "weight_kg", "weight_gap_kg"]].to_string(index=False))