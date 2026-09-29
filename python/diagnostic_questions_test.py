import json
import urllib.request


customer_facts = {
    "vehicle": {
        "make": "Volkswagen",
        "model": "Golf",
        "year": 2018,
    },
    "complaint": "The vehicle is difficult to start after driving for about 30 minutes.",
    "symptoms": [
        "struggles to start in the morning",
        "happens when the engine is cold",
    ],
    "warning_lights": [],
}


prompt = f"""
Return JSON only.

You are a Virtual Automotive Customer Service Assistant.

Your job is to ask ONE useful follow-up question
to collect information from a customer.

The vehicle has NOT been physically inspected.

Use only the customer information provided below.

Important rules:

- Ask exactly ONE question.
- Do not diagnose the vehicle.
- Do not suggest a repair.
- Do not assume the cause of the problem.
- Do not assume the weather is cold or hot.
- Ask about the engine condition rather than assuming the weather.
- The question must be useful for later diagnostic reasoning.
- Keep the question simple enough for a normal vehicle owner.
- Do not ask for information the customer has already provided.

Choose the follow-up question based on the information
that is already known.

Do not automatically ask about cold or warm engine
conditions.

Only ask about engine temperature if the customer's
existing information does not already tell us whether
the problem happens with a cold or warm engine.

The question must target ONE important piece of information
that is currently missing.

For starting problems, consider these information categories:

1. Starting behaviour:
   - Does the engine turn over normally?
   - Does it turn over slowly?
   - Does it not turn over at all?

2. Engine condition:
   - Cold
   - Already warm
   - Both

3. Frequency:
   - Every time
   - Sometimes
   - Rarely

4. Warning lights:
   - Warning light present
   - No warning light

5. What happens after attempting to start:
   - Eventually starts
   - Does not start
   - Starts and then stalls

Choose the category that provides the most useful missing
information based on what the customer has already told us.

Important:

The customer has already said the vehicle is difficult to
start after driving for about 30 minutes.

Treat this as information about WHEN the problem occurs.
Do not ask the customer to repeat when the problem occurs.

Do not assume that 30 minutes of driving proves the engine
is warm. If engine temperature is important and genuinely
unknown, it may still be asked about.

However, prefer other important missing information when
the customer's description already provides useful
information about the timing or circumstances.

Do not ask about a category if the customer has already
provided that information.

Do not automatically choose engine condition.

Use simple words and give the customer clear choices
where possible.

For example, if engine temperature is genuinely unknown:
"When this happens, is the engine cold, already warm,
or does it happen in both conditions?"
Do not repeat information that the customer has already provided.

For example, if the customer has already said the problem
happens in the morning, do not ask when the problem happens.
Instead, ask about the engine condition.

Return exactly this JSON structure:

{{
    "question": "your single question"
}}

Customer information:

{json.dumps(customer_facts, indent=2)}
"""


payload = {
    "model": "qwen3:1.7b",
    "prompt": prompt,
    "stream": False,
    "think": False,
}


request = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
)


response = urllib.request.urlopen(request, timeout=60)
result = json.loads(response.read().decode())

print("Raw AI response:")
print(result["response"])