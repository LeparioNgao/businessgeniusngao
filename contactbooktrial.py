contacts = [
    {
        "name": "Leuyan Lepario",
        "phone": "0755667788",
        "skill": "Roofer",
        "city": "Narok"
    },
    {
        "name": "Leonidas King",
        "phone": "0722334526",
        "skill": "electrician",
        "city": "Nairobi"
    },
    {
        "name": "Synthia Wanjiru",
        "phone": "0760456321",
        "skill": "copywriting",
        "city": "Narok"
    },
    {
        "name": "John Doe",
        "phone": "0789654321",
        "skill": "masonry",
        "city": "Nairobi"
    },
]
#Adding a contact

contacts.append({
    "name": "Winnie Musungu",
    "phone": "0743521768",
    "skill": "Baking",
    "city": "Kisumu"
})

#Display all contacts

print("==== CONTACT BOOK ====")
for i, contact in enumerate(contacts):
    print(f"\n{i + 1}. {contact['name']}")
    print(f" Phone : {contact['phone']}")
    print(f" Skill : {contact['skill']}")
    print(f" City : {contact['city']}")

#Search by city
search_city = "Narok"
print(f" Contacts in {search_city}: ")

for contact in contacts:
    if contact["city"] == search_city:
        print(f" {contact['name']} | {contact['phone']} | {contact['skill']}")