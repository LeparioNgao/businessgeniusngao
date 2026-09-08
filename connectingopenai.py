#scikit-learn trains models on your own data.
# The OpenAI API lets you send any text to a pre-trained language model and get back a generated response.
# These are two different kinds of intelligence working together.
# This lesson covers how to structure OpenAI API calls and how to use them in production scripts.

#Learning Objectives
# 1. Understand how the OpenAI chat API works
# 2. Structure messages with system and user roles
# 3. Extract the response text from the API return value
# 4. Use a system prompt to shape the AI output
# 5. Build a multi-turn conversation structure
# 6. Use the API to extract structured data from text

#The OpenAI API requires an active key and makes live network calls.
# The browser terminals simulate the API structure and response format using hardcoded Python dicts so you can learn the code pattern without spending API credits.
# The VS Code blocks show the exact production code.

# 1. How the Chat API Works.
#The OpenAI Chat API accepts a list of messages (a conversation history) and returns the model's next message.
# Each message has a role (system, user, or assistant) and content (the text).
# The model reads the full conversation history and generates the next assistant turn.

# In VS Code (requires: pip install openai, python-dotenv)

#from openai import OpenAI
#from dotenv import load_dotenv
#import os

#load_dotenv()
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#response = client.chat.completions.create(
 #   model="gpt-4o-mini",
  #  messages=[
   #     {"role": "system", "content": "You are a direct, no-nonsense fitness coach."},
   #     {"role": "user",   "content": "James slept 6 hours and hit 7800 steps. What should he do tomorrow?"}
  #  ]
#)

# Extract the text
#reply = response.choices[0].message.content
#print(reply) 
#
# 2. Simulating the API Response Structure.
# Simulates the object that response.choices[0].message.content extracts from
# This mirrors the actual OpenAI API response structure exactly

class Message:
    def __init__(self, content):
        self.content = content
        self.role = "assistant"

class Choice:
    def __init__(self, content):
        self.message = Message(content)

class SimulatedResponse:
    def __init__(self, content):
        self.choices = [Choice(content)]
        self.model = "gpt-4o-mini"
        self.usage = {"prompt_tokens": 45, "completion_tokens": 82, "total_tokens": 127}

# Simulated response as if the API returned it
sim_response = SimulatedResponse(
    "Sleep was the limiting factor today. James hit 7,800 steps but 6 hours is below optimal. "
    "Tomorrow: prioritize 8+ hours tonight. Keep the step target at 9,000, not 10,000, "
    "since recovery is still incomplete. Add a 20-minute walk after lunch to hit it without needing a long session."
)

# Extract the reply (same code you use with the live API)
reply = sim_response.choices[0].message.content
print("AI Coach Response:")
print(reply)
print(f"\nTokens used: {sim_response.usage['total_tokens']}")

# 3. Using a System Prompt.
#The system message tells the model its role, tone, and constraints before the conversation starts.
# It is the most powerful tool for shaping the output.

import json

# Different system prompts produce different outputs for the same user message
system_prompts = {
    "SMP Coach": (
        "You are a strict SMP fitness coach. Be direct, no fluff. "
        "Give one actionable recommendation per response. Max 3 sentences."
    ),
    "Data Analyst": (
        "You are a fitness data analyst. Focus on numbers and trends. "
        "Output structured observations, not advice."
    ),
    "Nutritionist": (
        "You are a nutritionist specializing in intermittent fasting protocols. "
        "Focus only on eating patterns and timing."
    )
}

user_message = "James: steps=7800, sleep=6hr, protocol=OMAD, water=5 glasses, day 3 of deficit."

# Simulated responses for each system prompt
simulated_responses = {
    "SMP Coach": (
        "Six hours of sleep on day 3 of a deficit is why the steps are low. "
        "Tonight, sleep must be 8+ hours. Tomorrow target 9,000 steps only."
    ),
    "Data Analyst": (
        "Observation: Steps 22% below 10k goal. Sleep deficit likely compounding protocol fatigue. "
        "Water intake at 5/8 target. Recommend tracking energy levels as a leading indicator."
    ),
    "Nutritionist": (
        "Day 3 of OMAD with sleep deficit suggests cortisol is elevated. "
        "Consider shifting to 2MAD tomorrow to reduce stress load and support recovery."
    )
}

for role, prompt in system_prompts.items():
    print(f"[{role}]")
    print(f"  System: {prompt[:60]}...")
    print(f"  Response: {simulated_responses[role]}")
    print()

# 4. Multi-Turn Conversation.
#Each call to the API is stateless.
# To maintain a conversation, you build the messages list yourself, appending each turn as it happens.

def simulate_ai_response(messages):
    """Simulates what the OpenAI API returns based on the last user message."""
    last_user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")

    if "7800" in last_user_msg or "low" in last_user_msg.lower():
        return "Sleep was the limiter today. Prioritize 8+ hours tonight and target 9,000 steps tomorrow."
    elif "bench" in last_user_msg.lower() or "88" in last_user_msg:
        return "88kg bench on deficit sleep is strong. Deload to 80% next session to protect the joints."
    elif "protocol" in last_user_msg.lower() or "OMAD" in last_user_msg:
        return "OMAD works on high-sleep days. On sub-7 sleep, consider 2MAD to reduce cortisol load."
    else:
        return "Noted. Keep tracking and adjust the inputs. Consistency over perfection."

# Build conversation manually (what your script would maintain)
conversation = [
    {"role": "system", "content": "You are a direct SMP fitness coach. Max 2 sentences per reply."}
]

user_inputs = [
    "James hit 7800 steps today and slept 6 hours. OMAD protocol, day 3.",
    "He also hit a bench press PR of 88kg despite the deficit.",
    "Should he switch from OMAD to 2MAD tomorrow?"
]

print("=== Conversation ===\n")
for user_msg in user_inputs:
    # Add user message
    conversation.append({"role": "user", "content": user_msg})
    print(f"User: {user_msg}")

    # Simulate AI response
    reply = simulate_ai_response(conversation)

    # Add assistant reply to history
    conversation.append({"role": "assistant", "content": reply})
    print(f"Coach: {reply}\n")


# 5. Extracting Structured Data.
#Tell the model to respond in JSON.
# Parse the response with json.loads() to get a Python dictionary.
# This lets you use AI output programmatically.

import json

# System prompt requesting JSON output
system = """You are a fitness data extractor.
Parse the user's daily log and return ONLY valid JSON with these keys:
steps (int), sleep_hours (float), protocol (str), cold_shower (bool), water_glasses (int).
No other text."""

# What the AI would return for this input
raw_log = "Today I did 15000 steps, slept for 8 hours, followed 2MAD, took a cold shower and drank 8 glasses of water."

# Simulated AI JSON response
simulated_json_response = '{"steps": 15000, "sleep_hours": 8, "protocol": "2MAD", "cold_shower": true, "water_glasses": 8}'

# Parse it
try:
    parsed = json.loads(simulated_json_response)
    print("Parsed structured data:")
    for key, value in parsed.items():
        print(f"  {key}: {value}")

    # Use it programmatically
    print()
    if parsed["steps"] >= 10000:
        print("Step goal: HIT")
    else:
        print(f"Step goal: {parsed['steps']:,}/10,000 ({10000 - parsed['steps']:,} short)")
    print(f"Sleep rating: {'Good' if parsed['sleep_hours'] >= 7.5 else 'Low'}")

except json.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")