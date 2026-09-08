import urllib.request, json
# Make a request with a custom header
req = urllib.request.Request(
    "https://httpbin.org/headers/",
    headers={"X-Custom-Header": "AmerixMasterclass"}
)
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read())
print(data["headers"])
