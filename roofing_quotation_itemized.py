import pandas as pd

CSV_PATH = "roofing_materials.csv"

ITEMS = [
    "ngao_platinum_tile",
    "ridge",
    "valley_iron",
    "abc",
    "swf",
    "roofing_nails",
    "repair_kit",
]


def load_prices(csv_path=CSV_PATH):
    df = pd.read_csv(csv_path)
    price_map = df.set_index("material")["unit_price"].to_dict()

    price_map.setdefault("ngao_platinum_tile", 850)
    price_map.setdefault("ridge", 1000)
    price_map.setdefault("valley_iron", 1000)
    price_map.setdefault("abc", 1000)
    price_map.setdefault("swf", 1000)
    price_map.setdefault("roofing_nails", 850)
    price_map.setdefault("repair_kit", 850)
    price_map.setdefault("labour", 15000)

    return price_map


def itemized_quote():
    prices = load_prices()
    print("Ngao Roofing Itemized Quotation")
    print("-" * 60)

    line_items = []
    total = 0

    for item in ITEMS:
        qty = float(input(f"Enter quantity for {item.replace('_', ' ').title()}: "))
        unit_price = prices.get(item, 0)
        amount = qty * unit_price
        line_items.append((item, qty, unit_price, amount))
        total += amount

    labour = float(input("Enter labour cost: "))
    total += labour

    print("\nQuotation breakdown")
    print("-" * 60)
    for item, qty, unit_price, amount in line_items:
        print(f"{item.replace('_', ' ').title():20} Qty: {qty:>6} @ KES {unit_price:,.0f} = KES {amount:,.0f}")

    print(f"{'Labour':20} Qty: {'-':>6} @ KES {'-':>8} = KES {labour:,.0f}")
    print("-" * 60)
    print(f"{'TOTAL':20} KES {total:,.0f}")


if __name__ == "__main__":
    itemized_quote()
