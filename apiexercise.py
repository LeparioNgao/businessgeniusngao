import os
import sys
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        print("WEATHER_API_KEY not found in environment variables.")
        sys.exit(1)
    return api_key

print("API Key:", get_api_key())