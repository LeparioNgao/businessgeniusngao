# Majuwa Dairy Farm

A small machine-learning demonstration for dairy-farm planning. It generates simulated herd records, predicts milk yield, estimates health-alert risk, and prints a seven-day milk and feed forecast.

## Requirements

- Python 3.10 or later
- NumPy
- scikit-learn

## Setup

Run these commands from the repository root, the directory containing `majuwadairyfarm.py` and `majuwadairyfarm2.py`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install numpy scikit-learn
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1` instead of the `source` command. Use `py` in place of `python3` if that is the Python launcher installed on your system.

## Run

The main end-to-end simulation and operations report:

```bash
python majuwadairyfarm2.py
```

The smaller feed-and-lactation classifier example:

```bash
python majuwadairyfarm.py
```

Both scripts print results to the terminal. The main simulation uses a fixed random seed, so its generated data and report are reproducible with the same dependency versions.

## What It Does

`majuwadairyfarm2.py` creates records for 40 simulated cows over 180 days, trains a `RandomForestRegressor` for milk yield and a `RandomForestClassifier` for health-alert risk, evaluates both models on a held-out split, then reports sample cow checks and seven-day milk/feed projections. It generates the forecast data each time it runs; it does not read or write farm records.

`majuwadairyfarm.py` trains a separate small classifier on 20 hardcoded example observations and predicts whether three sample cows are above a 15-litre target.

## Limitations

All observations and labels are synthetic examples, not Majuwa Dairy Farm records. The health output is a model-generated alert estimate, not a diagnosis. Neither script is validated for veterinary, nutrition, financial, or live operating decisions. Real deployment would require consented farm data, domain review, and validation against actual outcomes.

## Scope Boundary

A revision would correct an agreed in-scope result such as a broken forecast, while a new feature would add out-of-scope functionality such as importing the farm's live CSV records and quoting the work separately.

## Project Files

- `majuwadairyfarm.py`: small yield-target classifier example
- `majuwadairyfarm2.py`: simulated herd, model evaluation, and operations report
- `DELIVERY_MESSAGE.md`: client-facing delivery note
