import pandas as pd

CSV_PATH = "roofing_materials.csv"


def load_prices():
    df = pd.read_csv(CSV_PATH)
    return df.set_index("material")["unit_price"].to_dict()


def manual_quotation():
    print("Ngao Roofing Manual Quotation Entry")
    print("-" * 50)
    print("Enter the values as they are normally written in the quotation book.")

    customer_name = input("Customer name: ").strip()
    roof_area_m2 = float(input("Roof area in m²: "))
    tiles_needed = int(input("Tiles needed: "))
    accessories_meters = int(input("Accessories length in metres: "))
    touch_up_boxes = int(input("Touch-up kits: "))
    nails_kg = int(input("Serrated nails in kg: "))

    prices = load_prices()

    tile_cost = tiles_needed * prices.get("ngao_platinum_tile", 850)
    accessories_cost = accessories_meters * prices.get("accessories", 1200)
    touch_up_cost = touch_up_boxes * prices.get("touch_up_kit", 1200)
    nails_cost = nails_kg * prices.get("serrated_nails", 1200)
    labour_cost = prices.get("labour", 15000)

    materials_cost = tile_cost + accessories_cost + touch_up_cost + nails_cost
    total_cost = materials_cost + labour_cost

    print("\nManual quotation summary")
    print("-" * 50)
    print(f"Customer: {customer_name}")
    print(f"Roof area: {roof_area_m2} m²")
    print(f"Tiles: {tiles_needed}")
    print(f"Accessories: {accessories_meters} m")
    print(f"Touch-up kits: {touch_up_boxes}")
    print(f"Serrated nails: {nails_kg} kg")
    print(f"Materials cost: KES {materials_cost:,}")
    print(f"Labour cost: KES {labour_cost:,}")
    print(f"Total quotation: KES {total_cost:,}")
    print("\nYou can now copy these values into the main quoting calculator and compare the result.")


if __name__ == "__main__":
    manual_quotation()
