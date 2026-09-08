#Building a contact book
contacts = [
    {
        "name": "James Omondi",
        "phone": "0721345678",
        "skill": "welding",
        "city": "Nairobi"
    },
    {
        "name": "Sandra Weru",
        "phone": "0723456789",
        "skill": "tiling",
        "city": "Mombasa"
    },
    {
        "name": "Patrick Njiru",
        "phone": "0734567980",
        "skill": "phone repair",
        "city": "Nairobi"
    },
    {
        "name": "Grace Achieng",
        "phone": "0745678901",
        "skill": "copywriting",
        "city": "Kisumu"
    },
    {
        "name": "Brian Kamau",
        "phone": "0756789012",
        "skill": "upholstery",
        "city": "Nairobi"
    },
]

print("Contacts stored", len(contacts))
print(contacts[0])

#printing the contacts in a neat way to make it easy for display and reading
print("==== CONTACT BOOK ====")
for i, contact in enumerate(contacts):
    print(f"\n{i + 1}. {contact['name']}")
    print(f" Phone : {contact['phone']}")
    print(f" Skill : {contact['skill']}")
    print(f" City : {contact['city']}")

#Search for a contact
search_name = "Lepario Ngao"
found = False

for contact in contacts:
    if contact["name"] == search_name:
        print("Contact found: ")
        print(f" Name : {contact['name']}")
        print(f" Phone : {contact['phone']}")
        print(f" Skill : {contact['skill']}")
        print(f" City : {contact['city']}")
        found = True
        break
if not found:
    print("No contact found with the name:", search_name)

#Search by city
search_city = "Nairobi"
print(f" Contacts in {search_city}: ")

for contact in contacts:
    if contact["city"] == search_city:
        print(f" {contact['name']} | {contact['skill']} | {contact['phone']}")

print("Before:", len(contacts), "contacts")

#Adding a new contact
new_contact = {
    "name": "Kevin Mwangi",
    "phone": "0767890123",
    "skill": "beekeeping",
    "city": "Nakuru"
}
contacts.append(new_contact)

print("After:", len(contacts), "contacts")
print("Last contact: ", contacts[-1])