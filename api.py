# In VS Code (requires: pip install requests)
import requests

# A free public API that returns JSON data
url = "https://jsonplaceholder.typicode.com/users/1"

response = requests.get(url)

print("Status Code:", response.status_code)
data = response.json()
print("User Data:", data)


import requests

# A free public API that returns JSON data
url = "https://jsonplaceholder.typicode.com/users/1"

response = requests.get(url)

print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()  # Parses the JSON response into a Python dictionary
    
    # Accessing specific fields from the JSON response
    print("User Name:", data["name"])
    print("Email:", data["email"])
    print("City:", data["address"]["city"])
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")