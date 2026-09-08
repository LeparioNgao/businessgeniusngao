# Analyze 28 days of dairy farm milk production data using pandas and NumPy.

import numpy as np
import pandas as pd


# Step 1: Load and inspect one month's milk records.
data = {
    "day": list(range(1, 29)),
    "milk_litres": [420, 438, 415, 452, 398, 431, 445,
                    425, 449, 418, 461, 405, 447, 436,
                    432, 455, 421, 468, 412, 443, 459,
                    429, 452, 417, 464, 409, 448, 456],
    "fat_pct": [3.8, 3.9, 3.7, 4.0, 3.6, 3.8, 3.9,
                3.8, 4.0, 3.7, 4.1, 3.6, 3.9, 3.8,
                3.8, 4.0, 3.7, 4.1, 3.6, 3.9, 4.0,
                3.8, 4.0, 3.7, 4.1, 3.6, 3.9, 4.0],
    "protein_pct": [3.2, 3.3, 3.2, 3.4, 3.1, 3.2, 3.3,
                    3.2, 3.4, 3.2, 3.5, 3.1, 3.3, 3.2,
                    3.2, 3.4, 3.2, 3.5, 3.1, 3.3, 3.4,
                    3.2, 3.4, 3.2, 3.5, 3.1, 3.3, 3.4],
    "feed_kg": [218, 220, 216, 224, 212, 219, 222,
                218, 223, 217, 226, 213, 222, 220,
                219, 224, 216, 228, 214, 221, 225,
                218, 223, 215, 227, 213, 222, 224],
    "protocol": (["Pasture", "Mixed", "Pasture", "Mixed", "Pasture", "Mixed", "Mixed"] * 4),
    "cows_milked": [48, 49, 47, 50, 46, 48, 49,
                    48, 50, 47, 51, 46, 49, 48,
                    48, 50, 47, 51, 46, 49, 50,
                    48, 50, 47, 51, 46, 49, 50],
}
df = pd.DataFrame(data)

print(f"Shape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")
print("\nData types:")
print(df.dtypes)
print(f"\nMissing values: {df.isna().sum().sum()}")
print("\nFirst 3 rows:")
print(df.head(3).to_string(index=False))


# Step 2: Filter high-yield days and compare feeding protocols.
high_yield = df[(df["milk_litres"] >= 450) & (df["fat_pct"] >= 4.0)]
print(f"\nHigh-yield days: {len(high_yield)}/28")

print("\nMetrics by feeding protocol:")
protocol_stats = df.groupby("protocol").agg(
    avg_milk_litres=("milk_litres", "mean"),
    avg_fat_pct=("fat_pct", "mean"),
    avg_protein_pct=("protein_pct", "mean"),
    avg_feed_kg=("feed_kg", "mean"),
    days=("day", "count"),
).round(1)
print(protocol_stats)


# Step 3: NumPy statistics, correlation, and trend analysis.
milk = np.array(data["milk_litres"])
feed = np.array(data["feed_kg"])
fat = np.array(data["fat_pct"])

print("\n=== 28-Day NumPy Milk Analysis ===")
print("\nMilk production:")
print(f"  Mean:        {np.mean(milk):,.1f} litres")
print(f"  Std dev:     {np.std(milk):,.1f} litres")
print(f"  25th pctile: {np.percentile(milk, 25):,.1f} litres")
print(f"  75th pctile: {np.percentile(milk, 75):,.1f} litres")
print(f"  Days 450+:   {np.sum(milk >= 450)}/28")

print("\nMilk quality:")
print(f"  Average fat: {np.mean(fat):.1f}%")
print(f"  Best day:    {np.max(milk):,.0f} litres (Day {np.argmax(milk) + 1})")
trend_change = milk[-7:].mean() - milk[:7].mean()
print(f"  Trend:       {trend_change:+.1f} litres (week 1 to week 4)")

corr = np.corrcoef(feed, milk)[0, 1]
print(f"\nCorrelation feed vs milk: {corr:.3f}")
print("Interpretation:", "positive relationship" if corr > 0.3 else "weak/no relationship")


# Step 4: Full formatted report.
W = 58
print("\n" + "=" * W)
print("  DAIRY FARM 28-DAY MILK ANALYSIS REPORT")
print("=" * W)

print("\n  OVERALL METRICS")
print(f"  {'Days tracked:':<27} 28")
print(f"  {'Total milk collected:':<27} {milk.sum():,.0f} litres")
print(f"  {'Average daily production:':<27} {milk.mean():,.1f} litres")
print(f"  {'Days producing 450+ litres:':<27} {(milk >= 450).sum()}/28 ({(milk >= 450).mean() * 100:.0f}%)")
print(f"  {'Average fat content:':<27} {fat.mean():.1f}%")
print(f"  {'Milk production range:':<27} {milk.min()} to {milk.max()} litres")
print(f"  {'Production trend:':<27} {trend_change:+.1f} litres (week 1 to week 4)")

print("\n  WEEKLY BREAKDOWN")
print(f"  {'Week':<8} {'Avg Milk':>12}  {'450+ Days':>10}  {'Avg Feed':>10}")
print(f"  {'-' * 46}")
for week in range(4):
    milk_week = milk[week * 7:(week + 1) * 7]
    feed_week = feed[week * 7:(week + 1) * 7]
    hits = (milk_week >= 450).sum()
    print(f"  Week {week + 1:<3} {milk_week.mean():>12,.1f}  {hits:>10}/7  {feed_week.mean():>9.1f} kg")

print("\n  FEEDING PROTOCOL COMPARISON")
for protocol, row in protocol_stats.iterrows():
    print(f"  {protocol}: milk={row['avg_milk_litres']:,.1f} litres, "
          f"fat={row['avg_fat_pct']:.1f}%, feed={row['avg_feed_kg']:.1f} kg")

print("\n  TOP 3 MILK PRODUCTION DAYS")
for _, row in df.nlargest(3, "milk_litres").iterrows():
    print(f"  Day {int(row['day']):2d}: {int(row['milk_litres']):,} litres "
          f"({row['protocol']} protocol, {row['cows_milked']} cows)")

print(f"\n{'=' * W}")