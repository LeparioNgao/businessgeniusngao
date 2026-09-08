import json
# Mock response that simulates a public API
data = {
    "userId": 1,
    "id": 2,
    "title": "qui est esse",
    "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea"
}
print(json.dumps(data, indent=2))

import json
# Parse this nested JSON and print the author and title
response = '{"book": {"title": "Clean Code", "author": "Robert Martin", "year": 2008}}'
data = json.loads(response)
book = data["book"]
print(f"Title: {book['title']}")
print(f"Author: {book['author']}")


import json
# Mock response that simulates httpbin.org/headers/ API response
# (demonstrating how headers would be echoed back)
data = {
    "headers": {
        "Host": "httpbin.org",
        "X-Custom-Header": "AmerixMasterclass",
        "User-Agent": "Python-urllib/3.14"
    }
}
print(data["headers"])

import urllib.request, json
# Fetch a joke from a public API and print it
url = "https://official-joke-api.appspot.com/random_joke"
try:
    with urllib.request.urlopen(url, timeout=5) as r:
        joke = json.loads(r.read())
    print(joke['setup'])
    print(joke['punchline'])
except Exception as e:
    print(f"Could not fetch joke: {e}")

import json

# Simulated API response from a steel supplier
response_text = '''
{
    "supplier": "Nairobi Steel Ltd",
    "date": "2026-07-27",
    "prices": {
        "mild_steel_sheet": 4500,
        "angle_iron": 2800,
        "square_tube": 3200
    },
    "currency": "KES",
    "unit": "per metre"
}
'''

data = json.loads(response_text)

print(f"Supplier: {data['supplier']}")
print(f"Date: {data['date']}")
print(f"\nSteel prices ({data['currency']} {data['unit']}):")
for item, price in data["prices"].items():
    print(f"  {item.replace('_', ' ').title()}: KES {price:,}")

# One steel door frame: 3 pieces of angle iron (2m each) + 1 mild steel sheet
angle_cost = data["prices"]["angle_iron"] * 2 * 3
sheet_cost = data["prices"]["mild_steel_sheet"]
frame_cost = angle_cost + sheet_cost

print(f"\nDoor frame quote:")
print(f"  Angle iron (3 x 2m): KES {angle_cost:,}")
print(f"  Mild steel sheet: KES {sheet_cost:,}")
print(f"  Total: KES {frame_cost:,}")