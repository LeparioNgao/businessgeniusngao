#Using the JSON placeholder API, we can get a list of users. Each user has a name and an address. The address is a nested dictionary with street, city, and zipcode.
#We want to build a clean list of just the names and cities.

clean_users = []
for user in users:
    name = user["name"]
    city = user["address"]["city"]
    clean_users.append({"name": name, "city": city})   

