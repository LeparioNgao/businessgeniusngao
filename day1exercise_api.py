import requests

URL = "https://jsonplaceholder.typicode.com/users/1"

response = requests.get(URL, timeout=20)

if response.ok:
	user = response.json()
	print("User Profile Summary")
	print("-" * 25)
	print(f"Name: {user['name']}")
	print(f"Username: {user['username']}")
	print(f"Email: {user['email']}")
	print(f"Phone: {user['phone']}")
	print(f"Website: {user['website']}")
	print(f"Address: {user['address']['street']}, {user['address']['city']}, {user['address']['zipcode']}")
	print(f"Company: {user['company']['name']}")
	print(f"Catchphrase: {user['company']['catchPhrase']}")
else:
	print("Request failed. Status:", response.status_code)
