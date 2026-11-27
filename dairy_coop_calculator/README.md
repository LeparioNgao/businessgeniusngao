# Dairy Co-op Payment Calculator v1.0

## What this does

This command-line tool calculates a farmer's milk payment from:

- the weekly buying price in `price.txt`;
- the farmer's name; and
- the litres supplied today.

It is designed for a small co-op and does not require a website or database.

## Step 1: Check Python

Open a terminal and confirm Python is available:

```bash
python3 --version
```

Python 3.8 or newer is sufficient.

## Step 2: Open the package

```bash
cd dairy_coop_calculator
```

## Step 3: Update the weekly price

Open `price.txt` and replace the number with the current KES buying price. Keep only the number in the file, for example:

```text
55.0
```

## Step 4: Run the calculator

```bash
python3 dairy_calculator.py
```

## Example output

```text
Kiambu Dairy Co-op Payment Calculator
--------------------------------------
Current buying price: KES 55.00 per litre

Farmer name: Wanjiku
Litres supplied today: 18.5

Payment Summary
---------------
Farmer : Wanjiku
Litres : 18.5
Price  : KES 55.00/litre
Total  : KES 1,017.50
```

## Invalid-input behaviour

- An empty name prints `Name is required.`
- Zero or negative litres print `Litres must be greater than zero.`
- Text such as `letters` prints `Please enter a valid number for litres.`

## Step 5: Run tests

```bash
python3 -m unittest test_dairy_calculator.py
```

The tests cover three example payments, the current price file, zero/negative litres, and invalid text conversion.

## Scope

Version 1.0 calculates and displays one current payment. It does not store payment history or export month-end reports.
