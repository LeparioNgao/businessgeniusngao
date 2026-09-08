#An API key is a unique string that identifies your application to an API. It tells the server who is making the request, lets the provider track and limit usage, and prevents unauthorized access to paid or sensitive data.

#Never put an API key directly in your code.
#If you paste a key as a string in your script and push that script to GitHub, the key becomes public. Automated bots scan GitHub continuously for leaked keys and will use or sell them within minutes. Always load keys from outside your code.

# WRONG: key hardcoded in script
#api_key = "sk-abc123yourrealkeyhere"
#response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})

#Method 1: Environment Variables
#An environment variable is a value stored in your operating system, separate from your code. Your script reads it at runtime. The key never appears in your file.
# In Terminal (Mac/Linux) - temporary, lasts the session
#export OPENAI_API_KEY="sk-abc123yourrealkeyhere"

# In Command Prompt (Windows) - temporary
#set OPENAI_API_KEY=sk-abc123yourrealkeyhere

#os is a built-in Python module that lets your code interact with the operating system.
# You do not install it with pip because it is part of Python's standard library.
# import os gives you access to os.environ, a dictionary of all environment variables currently set on your system, and os.getenv("KEY"), a function that retrieves a single variable by name.
# This is how your Python script reads values that were set outside the script, such as keys stored in a .env file.


import os

# Simulate: key loaded from environment (not hardcoded)
os.environ["SMP_API_KEY"] = "smp_test_key_abc123"   # set for demo only

api_key = os.environ.get("SMP_API_KEY")

if not api_key:
    print("ERROR: API key not found. Set the SMP_API_KEY environment variable.")
else:
    # Show only first 8 chars for safety
    masked = api_key[:8] + "..." + api_key[-4:]
    print(f"Key loaded: {masked}")
    print("Ready to make authenticated requests.")


#Method 2: .env File(Recommended)
#A .env file stores key-value pairs in a text file in your project folder.
# You load it at runtime using the python-dotenv library. The file stays on your machine and never gets pushed to GitHub.

from dotenv import load_dotenv
import os

load_dotenv()   # reads .env and sets environment variables

api_key = os.getenv("SMP_API_KEY")
print(api_key)


from dotenv import load_dotenv
import os

load_dotenv()   # reads .env and sets environment variables

api_key = os.getenv("SMP_API_KEY")
print(api_key)

#Parsing keys in requests
#APIs accept keys in two main ways. Check the documentation for the specific API you are using.
#Method A: Query Parameter in the URL

# Key passed as a URL parameter
#url = f"https://api.weatherprovider.com/current?city=Nairobi&apikey={api_key}"
#response = requests.get(url)

#or
# Or using the params dict (cleaner)
#params = {
 #   "city": "Nairobi",
  #  "apikey": api_key
#}
#response = requests.get("https://api.weatherprovider.com/current", params=params)

#Method B: Authorization Header

#A Bearer token is a type of access credential sent in an HTTP request header to prove you are allowed to use an API.
# "Bearer" means the person holding (bearing) this token is authorised to make the request.
# You pass it in the Authorization header with the format Bearer YOUR_TOKEN_HERE.
# This is the authentication pattern used by OpenAI, X (Twitter), and most modern APIs.
# Your Bearer token is just as sensitive as a password: keep it in your .env file and never paste it into code you push to GitHub.

# Bearer token (used by OpenAI, many modern APIs)
#headers = {
 #   "Authorization": f"Bearer {api_key}",
  #  "Content-Type": "application/json"
#}
#response = requests.get(url, headers=headers)

# Or as a custom header (varies by API)
#headers = {"X-API-Key": api_key}
#response = requests.get(url, headers=headers)

import os

# Simulate: load key from environment
os.environ["SMP_API_KEY"] = "smp_live_abc123xyz"
api_key = os.getenv("SMP_API_KEY")

# Build request components (what you would pass to requests.get)
url = "https://api.smptracker.com/v1/members"
params = {"city": "Nairobi", "limit": 10}
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print("URL:", url)
print("Params:", params)
print("Auth header:", "Bearer " + api_key[:8] + "...")

# Simulate a 200 response
print()
print("Response status: 200")
print("Response body: { 'members': [...], 'total': 42 }")

#Handling Authentication Errors
#When authentication fails, the API returns a 401 or 403 status code. Always check the status before trying to use the response body.

def handle_api_response(status_code, body):
    if status_code == 200:
        return body
    elif status_code == 401:
        raise PermissionError("Authentication failed. Check your API key.")
    elif status_code == 403:
        raise PermissionError("Access denied. Your key does not have permission for this endpoint.")
    elif status_code == 429:
        raise RuntimeError("Rate limit exceeded. Wait before retrying.")
    elif status_code >= 500:
        raise RuntimeError(f"Server error ({status_code}). Try again later.")
    else:
        raise RuntimeError(f"Unexpected status: {status_code}")

# Test with different status codes
test_cases = [
    (200, {"members": [{"name": "James Omondi"}]}),
    (401, {"error": "invalid_key"}),
    (429, {"error": "rate_limit_exceeded"}),
    (500, {"error": "internal_server_error"}),
]

for status, body in test_cases:
    try:
        result = handle_api_response(status, body)
        print(f"Status {status}: OK, got {result}")
    except Exception as e:
        print(f"Status {status}: {e}")

#APIs limit how many requests you can make per minute, hour, or day. Exceeding the limit returns a 429 error. For high-volume scripts, add a delay between requests using time.sleep().

import time

# Simulate making multiple API calls with a delay
member_ids = [1, 2, 3, 4, 5]

def fetch_member(member_id):
    # Simulates what requests.get would return
    mock_data = {
        1: {"name": "James Omondi",  "steps": 9200},
        2: {"name": "Sandra Weru",   "steps": 10500},
        3: {"name": "Patrick Njiru", "steps": 8100},
        4: {"name": "Grace Achieng", "steps": 11000},
        5: {"name": "Brian Kamau",   "steps": 7400},
    }
    return mock_data.get(member_id)

results = []
for mid in member_ids:
    data = fetch_member(mid)
    results.append(data)
    print(f"Fetched: {data['name']} ({data['steps']} steps)")
    # In production: time.sleep(0.5) to avoid rate limits

print(f"\nTotal fetched: {len(results)}")

import os

# Step 1: Load the token from environment (never hardcode it)
os.environ["FB_ACCESS_TOKEN"] = "EAADemo_token_never_hardcode_real_ones"
token = os.getenv("FB_ACCESS_TOKEN")

# Step 2: This is what the Graph API returns for facebook.com/amerix041
fb_response = {
    "id": "100044385041",
    "name": "Amerix",
    "about": "Reproductive Health | Men's Health and Wellness",
    "fan_count": 284000,
    "followers_count": 291500,
    "category": "Health & Wellness Website",
    "link": "https://www.facebook.com/amerix041"
}

# Step 3: Parse it exactly as you have learned
name       = fb_response["name"]
about      = fb_response["about"]
fans       = fb_response["fan_count"]
followers  = fb_response["followers_count"]
page_link  = fb_response["link"]

print("FACEBOOK PAGE DATA")
print(f"  Page:       {name}")
print(f"  About:      {about}")
print(f"  Page likes: {fans:,}")
print(f"  Followers:  {followers:,}")
print(f"  Link:       {page_link}")
print()
print(f"Token loaded: {token[:12]}... (never log a live token)")
print()
print("Note: In production, replace the mock response with:")
print("  response = requests.get(url, params={'access_token': token, 'fields': '...'})")
print("  data = response.json()")

