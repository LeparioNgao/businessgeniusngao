# Majuwa Dairy Farm Project

A portfolio-ready machine learning project that uses a simulated dairy herd to predict milk output and flag health risks for cows. The project combines data generation, supervised learning, and simple forecasting to support farm planning decisions.

## Problem

A dairy farm needs to know how much milk to expect each day, how much feed to prepare, and which cows may need closer monitoring. Without a data-driven approach, decisions are based on guesswork, rough observation, and manual recordkeeping.

## Solution

This project builds a small end-to-end ML workflow:

- generates a realistic herd dataset for feed, lactation stage, temperature, and previous milk output
- trains a regression model to predict daily milk yield
- trains a classification model to estimate health risk probability
- forecasts the next 7 days of milk and feed demand
- prints a manager-friendly operations report

## Tools Used

- Python
- NumPy
- scikit-learn
- Random Forest Regressor
- Random Forest Classifier
- Jupyter-style script workflow

## Project Outcome

The model helps a farm manager plan production, estimate feed needs, and identify cows that may need inspection before a problem becomes serious. It is a teaching project designed to show how machine learning can support real-world agricultural decision-making.

## Key Features

- Herd simulation with 40 cows across 180 days of records
- Prediction of expected milk output per cow
- Health-risk classification for timely inspection
- Seven-day forecast for milk sales and feed requirements
- Clear terminal report for operational decisions

## How the Model Works

The project uses two machine learning models:

1. Milk Yield Model
   - Predicts expected litres of milk per cow
   - Uses features such as feed amount, lactation day, temperature, and prior milk yield
   - Built with `RandomForestRegressor`

2. Health Risk Model
   - Estimates the probability that a cow may require inspection
   - Uses the same feature set plus health-related conditions
   - Built with `RandomForestClassifier`

## Example Workflow

```bash
python majuwadairyfarm2.py
```

This prints a summary similar to:

```text
MAJUWA DAIRY FARM | ML OPERATIONS REPORT
Herd: 40 cows | Historical records: 7,200
Milk model: average error 1.23 litres per cow/day
Health model: test accuracy 84%

INDIVIDUAL COW CHECKS
Cow 01: 16.2 L expected | health risk 18% | Normal monitoring
Cow 12: 13.8 L expected | health risk 42% | Inspect today

SEVEN-DAY SALES AND FEED FORECAST
Day 181: 5,240 L milk | 780 kg feed
...
```

## Project Structure

```text
MACHINE LEARNING MASTERCLASS/
├── majuwadairyfarm.py
├── majuwadairyfarm2.py
├── README.md
└── ...
```

## Why This Is a Good Portfolio Project

This project shows that I can:

- work with structured data
- cleanly frame a real-world problem
- train and evaluate models
- turn model output into usable business insight
- explain results in clear, human-readable language

It is the kind of project that demonstrates practical machine learning thinking rather than only theory.

## Limitations

This is a simulated dataset, not real farm data. The project is educational and should not be used as a replacement for veterinary advice, farm nutrition planning, or live operational decisions. In a real production setting, this would need actual sensor, production, and health records.

## Future Improvements

- connect to a real CSV or database of farm records
- add visual dashboards for milk and health trends
- build a web interface for farm managers
- expand forecasting to include feed cost and revenue calculations
- add unit tests for the prediction logic

## Summary

Majuwa Dairy Farm demonstrates how machine learning can support agriculture by turning raw farm data into forecasting and decision support. It is a strong example of a practical Python project that fits well into a developer portfolio focused on data science and applied AI.
