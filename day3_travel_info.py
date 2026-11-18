"""
Travel Weather Tool
-------------------
Shows weather and country information for any city.

Usage:
    python day3_travel_info.py

Requirements:
    pip install requests python-dotenv
    OPENWEATHER_API_KEY in .env file
"""
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")


def save_to_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def get_country_info(country_code):
    url = f"https://restcountries.com/v3.1/alpha/{country_code}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and data:
            return data[0]
    return None


def run_tool():
    print("Travel Weather Tool")
    print("-------------------")
    city = input("Enter a city name: ").strip()

    if not city:
        print("No city entered. Exiting.")
        return

    print(f"\nFetching data for {city}...")

    weather_data = get_weather(city)

    if not weather_data:
        print(f"Could not find weather data for '{city}'. Check the city name and try again.")
        return
    save_to_file(weather_data, f"{city.lower()}_weather.json")

    country_code = weather_data["sys"]["country"]
    country_data = get_country_info(country_code)
    save_to_file(
        {"city": city, "weather": weather_data, "country": country_data},
        "travel_data.json",
    )

    print(f"\n=== {city.title()}, {country_code} ===")
    print(f"Temperature : {weather_data['main']['temp']}C")
    print(f"Condition   : {weather_data['weather'][0]['description'].title()}")
    print(f"Humidity    : {weather_data['main']['humidity']}%")
    print(f"Wind        : {weather_data['wind']['speed']} m/s")

    if country_data:
        population = country_data.get("population", 0)
        region = country_data.get("region", "Unknown")
        currencies = ", ".join(country_data.get("currencies", {}).keys())
        print(f"\n=== Country Info ===")
        print(f"Region      : {region}")
        print(f"Population  : {population:,}")
        print(f"Currency    : {currencies}")


run_tool()