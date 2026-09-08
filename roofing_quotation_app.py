import pandas as pd

CSV_PATH = "roofing_materials.csv"

ITEMS = [
    {"key": "ngao_platinum_tile", "label": "Ngao Platinum Tile", "unit": "each"},
    {"key": "ridge_cap", "label": "Ridge Cap", "unit": "each"},
    {"key": "iron_sheet", "label": "Iron Sheet", "unit": "each"},
    {"key": "wooden_batten", "label": "Wooden Batten", "unit": "each"},
    {"key": "accessories", "label": "Accessories", "unit": "meter"},
    {"key": "serrated_nails", "label": "Serrated Nails", "unit": "kg"},
    {"key": "touch_up_kit", "label": "Touch Up Kit", "unit": "box"},
    {"key": "roofing_felt", "label": "Roofing Felt", "unit": "roll"},
    {"key": "labour", "label": "Labour", "unit": "job"},
]


def load_prices(csv_path=CSV_PATH):
    df = pd.read_csv(csv_path)
    return df.set_index("material")["unit_price"].to_dict()


def quick_area_estimate(roof_area_m2, roofing_type="ngao_platinum_tile"):
    roof_area_m2 = float(roof_area_m2)
    prices = load_prices()

    tiles_needed = max(1, int(roof_area_m2 * 2))
    accessories_meters = max(1, int(roof_area_m2 * 0.4))
    touch_up_boxes = max(1, int(roof_area_m2 / 50))
    nails_kg = max(1, int(roof_area_m2 * 6))

    tile_cost = tiles_needed * prices.get("ngao_platinum_tile", 850)
    accessories_cost = accessories_meters * prices.get("accessories", 1200)
    touch_up_cost = touch_up_boxes * prices.get("touch_up_kit", 1200)
    nails_cost = nails_kg * prices.get("serrated_nails", 1200)
    labour_cost = prices.get("labour", 15000)

    total = tile_cost + accessories_cost + touch_up_cost + nails_cost + labour_cost
    return {
        "roof_area_m2": round(roof_area_m2, 2),
        "tiles_needed": tiles_needed,
        "accessories_meters": accessories_meters,
        "touch_up_boxes": touch_up_boxes,
        "nails_kg": nails_kg,
        "materials_cost": round(tile_cost + accessories_cost + touch_up_cost + nails_cost, 2),
        "labour_cost": labour_cost,
        "total_cost": round(total, 2),
    }


def calculate_itemized_quote(quantities):
    prices = load_prices()
    total = 0.0
    line_items = []

    for item in ITEMS:
        key = item["key"]
        qty = float(quantities.get(key, 0))
        unit_price = prices.get(key, 0)
        amount = qty * unit_price
        total += amount
        line_items.append({
            "label": item["label"],
            "key": key,
            "qty": qty,
            "unit_price": unit_price,
            "amount": amount,
        })

    return {
        "line_items": line_items,
        "total": total,
    }


def read_quantity(label, unit):
    try:
        value = input(f"Enter quantity for {label} ({unit}): ")
    except EOFError:
        return 0.0

    value = (value or "0").strip()
    if value == "":
        return 0.0
    return float(value)


def get_user_quantities():
    quantities = {}
    for item in ITEMS:
        value = read_quantity(item["label"], item["unit"])
        quantities[item["key"]] = value
    return quantities


if __name__ == "__main__":
    print("Ngao Roofing Quotation App")
    print("-" * 60)
    print("This version follows the office quotation method: item-by-item quantities and final total.")
    print("-" * 60)

    roof_area_m2 = float(input("Enter roof area in square metres (m²): "))
    quick_quote = quick_area_estimate(roof_area_m2)
    print("\nQuick area-based reference")
    print("-" * 60)
    print(f"Area: {quick_quote['roof_area_m2']} m²")
    print(f"Tiles: {quick_quote['tiles_needed']}")
    print(f"Accessories: {quick_quote['accessories_meters']} m")
    print(f"Touch-up kits: {quick_quote['touch_up_boxes']}")
    print(f"Nails: {quick_quote['nails_kg']} kg")
    print(f"Reference total: KES {quick_quote['total_cost']:,}")

    quantities = get_user_quantities()
    quote = calculate_itemized_quote(quantities)

    print("\nOffice-style quotation")
    print("-" * 60)
    for item in quote["line_items"]:
        print(f"{item['label']:<22} Qty {item['qty']:>8.0f} @ KES {item['unit_price']:>8,.0f} = KES {item['amount']:>12,.0f}")

    print("-" * 60)
    print(f"{'TOTAL':<22} KES {quote['total']:>12,.0f}")
