"""
Dairy Co-op Payment Calculator
-------------------------------
A small command-line tool for calculating a farmer's milk payment.

Step-by-step construction:
1. Read the weekly buying price from price.txt beside this script.
2. Validate the farmer name and litres supplied.
3. Multiply litres by the current price.
4. Print a clear KES payment summary.
"""

from pathlib import Path


DEFAULT_PRICE = 55.0
PRICE_FILE = Path(__file__).with_name("price.txt")


def get_current_price() -> float:
    """Read and validate the weekly price from price.txt."""
    try:
        price = float(PRICE_FILE.read_text(encoding="utf-8").strip())
        if price <= 0:
            raise ValueError("Price must be greater than zero")
        return price
    except (FileNotFoundError, ValueError):
        return DEFAULT_PRICE


def calculate_payment(litres: float, price_per_litre: float) -> float:
    """Calculate the amount owed for a supplied litre quantity."""
    if litres <= 0:
        raise ValueError("Litres must be greater than zero")
    if price_per_litre <= 0:
        raise ValueError("Price must be greater than zero")
    return litres * price_per_litre


def run() -> None:
    """Run the interactive command-line payment calculator."""
    print("Kiambu Dairy Co-op Payment Calculator")
    print("--------------------------------------")

    price = get_current_price()
    print(f"Current buying price: KES {price:.2f} per litre")

    # Step 1: accept and validate the farmer's name.
    name = input("\nFarmer name: ").strip()
    if not name:
        print("Name is required.")
        return

    # Step 2: accept and validate litres as a positive number.
    try:
        litres = float(input("Litres supplied today: ").strip())
        if litres <= 0:
            print("Litres must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number for litres.")
        return

    # Step 3: calculate and display the payment.
    total = calculate_payment(litres, price)
    print("\nPayment Summary")
    print("---------------")
    print(f"Farmer : {name}")
    print(f"Litres : {litres:g}")
    print(f"Price  : KES {price:.2f}/litre")
    print(f"Total  : KES {total:,.2f}")


if __name__ == "__main__":
    run()
