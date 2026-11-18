# Crypto Market Snapshot

A small command-line tool that gives a readable snapshot of a cryptocurrency's current price, market capitalization, 24-hour trading volume, and 24-hour price change. It combines data from CoinGecko's `/simple/price` and `/coins/markets` API endpoints, then saves the result as JSON for later use.

## Requirements

- Python 3
- A free CoinGecko Demo API key

## Setup

Install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Create or update a `.env` file in this folder or the repository root:

```text
COINGECKO_API_KEY=your-demo-api-key
```

The tool also recognizes `COINGECK_API_KEY` for compatibility with an existing key configured under that variable name. Never commit your `.env` file or share your key.

## Run

From this folder, run:

```bash
python3 crypto_market_tool.py
```

Enter a CoinGecko coin ID, such as `bitcoin`, `ethereum`, or `solana`, and a currency code such as `usd` or `eur`. The tool prints a summary and writes a file such as `bitcoin_market_snapshot.json` in this folder.

## Errors

The tool reports missing keys, invalid input, network failures, rejected API requests, rate limits, and missing coin data in plain language.

Market data can change and this tool is for learning purposes, not financial advice.
