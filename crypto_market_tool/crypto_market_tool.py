"""Crypto Market Snapshot

Fetch current price and market statistics for a cryptocurrency using CoinGecko.

Setup:
    Install dependencies with: python3 -m pip install -r requirements.txt
    Add COINGECKO_API_KEY=<your demo key> to a .env file in this folder or its parent.

Run:
    python3 crypto_market_tool.py
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

API_BASE_URL = "https://api.coingecko.com/api/v3"
OUTPUT_DIRECTORY = Path(__file__).resolve().parent


def api_get(endpoint, params, api_key):
    response = requests.get(
        f"{API_BASE_URL}/{endpoint}",
        params=params,
        headers={"x-cg-demo-api-key": api_key},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def fetch_market_snapshot(coin_id, currency, api_key):
    price_data = api_get(
        "simple/price",
        {"ids": coin_id, "vs_currencies": currency},
        api_key,
    )
    price = price_data.get(coin_id, {}).get(currency)
    if price is None:
        raise ValueError(f"No price data found for '{coin_id}'. Check the CoinGecko ID.")

    market_data = api_get(
        "coins/markets",
        {
            "vs_currency": currency,
            "ids": coin_id,
            "price_change_percentage": "24h",
        },
        api_key,
    )
    if not isinstance(market_data, list) or not market_data:
        raise ValueError(f"No market data found for '{coin_id}'. Check the CoinGecko ID.")

    market = market_data[0]
    return {
        "coin_id": coin_id,
        "name": market.get("name", coin_id.title()),
        "symbol": market.get("symbol", "").upper(),
        "currency": currency.upper(),
        "current_price": price,
        "market_cap": market.get("market_cap"),
        "total_volume_24h": market.get("total_volume"),
        "price_change_percentage_24h": market.get("price_change_percentage_24h"),
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def format_money(amount, currency):
    if amount is None:
        return "Not available"
    precision = 2 if abs(amount) >= 1 else 8
    return f"{currency} {amount:,.{precision}f}"


def display_snapshot(snapshot):
    currency = snapshot["currency"]
    print(f"\n{snapshot['name']} ({snapshot['symbol']})")
    print(f"Current price       {format_money(snapshot['current_price'], currency)}")
    print(f"Market capitalization {format_money(snapshot['market_cap'], currency)}")
    print(f"24-hour trading volume {format_money(snapshot['total_volume_24h'], currency)}")

    change = snapshot["price_change_percentage_24h"]
    if change is None:
        print("24-hour price change Not available")
    else:
        print(f"24-hour price change {change:+.2f}%")


def save_snapshot(snapshot):
    output_file = OUTPUT_DIRECTORY / f"{snapshot['coin_id']}_market_snapshot.json"
    with output_file.open("w", encoding="utf-8") as file:
        json.dump(snapshot, file, indent=2)
    print(f"\nSaved market snapshot to {output_file.name}")


def main():
    load_dotenv()
    api_key = os.getenv("COINGECKO_API_KEY") or os.getenv("COINGECK_API_KEY")
    if not api_key:
        print("CoinGecko API key not found. Add COINGECKO_API_KEY to your .env file.")
        return 1

    coin_id = input("Enter a CoinGecko coin ID (for example, bitcoin or ethereum): ").strip().lower()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", coin_id):
        print("Please enter a valid CoinGecko ID using letters, numbers, and hyphens.")
        return 1

    currency = input("Display currency [usd]: ").strip().lower() or "usd"
    if not re.fullmatch(r"[a-z]{3,5}", currency):
        print("Please enter a valid currency code, such as usd or eur.")
        return 1

    try:
        snapshot = fetch_market_snapshot(coin_id, currency, api_key)
    except requests.HTTPError as error:
        status_code = error.response.status_code if error.response is not None else "unknown"
        if status_code == 401:
            print("CoinGecko rejected the API key. Check your key in the .env file.")
        elif status_code == 429:
            print("CoinGecko's request limit was reached. Please try again later.")
        else:
            print(f"CoinGecko returned an error (HTTP {status_code}). Please try again later.")
        return 1
    except requests.RequestException:
        print("Could not connect to CoinGecko. Check your internet connection and try again.")
        return 1
    except ValueError as error:
        print(error)
        return 1

    display_snapshot(snapshot)
    try:
        save_snapshot(snapshot)
    except OSError:
        print("The data was fetched, but the JSON file could not be saved.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
