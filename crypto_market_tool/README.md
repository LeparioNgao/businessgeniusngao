# Crypto Market Snapshot

A command-line tool that combines a cryptocurrency's current price and market statistics from CoinGecko, converts USD values into a selected currency with ExchangeRate-API, prints a readable summary, and saves the result as JSON.

## Requirements

- Python 3
- A free CoinGecko Demo API key
- An ExchangeRate-API key to request a currency other than USD

## Setup

Install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Create or update a `.env` file in this folder or the repository root:

```text
COINGECKO_API_KEY=your-demo-api-key
EXCHANGERATE_API_KEY=your-exchange-rate-api-key
```

`EXCHANGERATE_API_KEY` is only used when you choose a non-USD currency. Never commit your `.env` file or share your keys.

## Run

From this folder, run:

```bash
python3 crypto_market_tool.py
```

Enter a CoinGecko coin ID, such as `bitcoin`, `ethereum`, or `solana`, and a display currency such as `usd`, `eur`, or `kes`. CoinGecko market data is fetched in USD; ExchangeRate-API converts the price, market capitalization, and trading volume when needed. The JSON snapshot includes both the original USD values and converted values.

## Errors

The tool reports missing keys, invalid input, network failures, rejected API requests, rate limits, and missing coin data in plain language.

Market data can change and this tool is for learning purposes, not financial advice.
