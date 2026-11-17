import os

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("EXCHANGERATE_API_KEY")
if not api_key:
    print("Add EXCHANGERATE_API_KEY to your .env file.")
else:
    try:
        codes_url = f"https://v6.exchangerate-api.com/v6/{api_key}/codes"
        codes_response = requests.get(codes_url, timeout=10)
        codes_response.raise_for_status()
        codes_data = codes_response.json()

        if codes_data.get("result") != "success":
            print(f"API error: {codes_data.get('error-type', 'unknown error')}")
            raise SystemExit

        currencies = {}
        for code, name in codes_data["supported_codes"]:
            currencies[code.casefold()] = code
            currencies[name.casefold()] = code

        currencies["kenya shillings"] = "KES"
        currencies["kenya shilling"] = "KES"

        base_input = input("Currency to exchange from (for example, Kenya shillings or KES): ").strip().casefold()
        target_input = input("Currency to exchange to (for example, USD or Euro): ").strip().casefold()
        base_currency = currencies.get(base_input)
        target_currency = currencies.get(target_input)

        if not base_currency or not target_currency:
            print("Currency not recognized or not supported by the API.")
            raise SystemExit

        amount = float(input("Amount to exchange: "))
        if amount <= 0:
            raise ValueError

        url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}/{amount}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data.get("result") == "success":
            print(
                f"{amount:g} {base_currency} = "
                f"{data['conversion_result']} {target_currency}"
            )
        else:
            print(f"API error: {data.get('error-type', 'unknown error')}")

    except requests.exceptions.JSONDecodeError:
        print("The API returned an invalid response.")
    except ValueError:
        print("Enter a valid positive amount.")
    except requests.exceptions.RequestException as error:
        print(f"Could not connect to the exchange-rate service: {error}")
    except KeyError:
        print("The API returned an invalid response.")
