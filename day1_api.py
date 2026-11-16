import requests

url = "https://api.worldbank.org/v2/country/GHA?format=json"

response = requests.get(url, timeout=15)
print("Status code:", response.status_code)

if response.ok:
    result = response.json()
    if len(result) < 2 or not result[1]:
        print("No country data was returned.")
        raise SystemExit(1)

    country = result[1][0]
    print("Data received:", country)

    print("Country:", country["name"])
    print("Capital:", country["capitalCity"])
    print("Region:", country["region"]["value"])
    print("Lending type:", country["lendingType"]["value"])
    print("Currency:", country.get("currencyCode", "Not available in this API"))
    print("Income level:", country["incomeLevel"]["value"])
else:
    print("Request failed. Status:", response.status_code)