#The system prompt defines what the AI does.
# Swap the SMP fitness coach prompt for a workshop quotation assistant and the API call structure is the same.
# Below simulates an AI that reads a client job request and returns a structured quote.

import json

# VS Code version would add two lines:
# from openai import OpenAI
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Then replace the simulated_responses below with a real client.chat.completions.create() call

workshop_system = """You are a Jua Kali workshop assistant for Kamau Metalworks, Gikomba.
When a client describes a job, return ONLY valid JSON with these keys:
  item (str), material (str), est_kes (int), days_to_complete (int), deposit_kes (int).
No other text."""

job_requests = [
    "I need a sliding gate, about 10 feet wide, mild steel.",
    "Window grills for three windows, 3x4 feet each, angle iron.",
    "A steel door frame for a standard door, hollow tube.",
]

# Simulated AI JSON responses
simulated_responses = [
    '{"item": "sliding gate", "material": "mild steel", "est_kes": 32000, "days_to_complete": 5, "deposit_kes": 16000}',
    '{"item": "window grills x3", "material": "angle iron", "est_kes": 21000, "days_to_complete": 3, "deposit_kes": 10500}',
    '{"item": "door frame", "material": "hollow tube", "est_kes": 9800, "days_to_complete": 2, "deposit_kes": 4900}',
]

print("Kamau Metalworks: AI Quotation Assistant\n")
for request, response_json in zip(job_requests, simulated_responses):
    print(f"Client: {request}")
    quote = json.loads(response_json)
    print(f"  Item:      {quote['item']}")
    print(f"  Material:  {quote['material']}")
    print(f"  Quote:     KES {quote['est_kes']:,}")
    print(f"  Deposit:   KES {quote['deposit_kes']:,}")
    print(f"  Ready in:  {quote['days_to_complete']} days")
    print()