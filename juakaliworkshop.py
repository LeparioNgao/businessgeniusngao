import pandas as pd

df = pd.DataFrame({
    "client":   ["Wanjiru", "Otieno", "Kamau", "Mwangi", "Njeri",  "Odhiambo", "Achieng", "Bett"],
    "item":     ["gate",    "grills", "frame", "gate",   "grills", "tank stand","frame",   "gate"],
    "material": ["mild steel","angle iron","hollow tube","mild steel","angle iron","mild steel","hollow tube","mild steel"],
    "region":   ["Nairobi", "Kiambu", "Machakos", "Nairobi", "Kiambu", "Machakos", "Kiambu", "Nairobi"],
    "price_kes":[28000, 14500, 9800, 32000, 12000, 18500, 11000, 29500],
    "status":   ["paid","paid","pending","paid","paid","pending","paid","paid"],
})

print("Revenue by material type:")
by_material = df.groupby("material")["price_kes"].agg(["sum","mean","count"]).round(0)
by_material.columns = ["total_kes", "avg_kes", "jobs"]
print(by_material.sort_values("total_kes", ascending=False).to_string())

print("\nPaid vs pending jobs:")
print(df["status"].value_counts())

print("\nAverage job value by status:")
print(df.groupby("status")["price_kes"].mean().round(0))

print("\nAverage earnings by region and material:")
by_region_material = df.groupby(["region", "material"])["price_kes"].agg(["mean", "count"]).round(0)
by_region_material.columns = ["avg_kes", "jobs"]
print(by_region_material.to_string())

top_region_by_material = by_region_material["avg_kes"].groupby(level="material").idxmax()
print("\nHighest-earning region per material:")
print(by_region_material.loc[top_region_by_material].to_string())