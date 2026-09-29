import json
import urllib.request


customer_facts = {
    "vehicle": {
        "make": "Volkswagen",
        "model": "Golf",
        "year": 2018,
    },
    "complaint": (
        "The vehicle is difficult to start after driving "
        "for about 30 minutes."
    ),
    "symptoms": [],
    "warning_lights": [],
    "starting_behaviour": "turns over slowly",
}


selected_information = "frequency"


def generate_question(selected_information):
    prompt = f"""
Return JSON only.

You are a Virtual Automotive Customer Service Assistant.

The application has already decided what information
needs to be collected.

Your job is ONLY to turn the selected information into
ONE simple customer-friendly question.

Do not decide what information is needed.

Do not diagnose the vehicle.

Do not suggest a repair.

Ask exactly ONE question.

Selected information:

{selected_information}

If the selected information is "frequency",
ask how often the starting problem happens.

Return exactly:

{{
    "question": "your single question"
}}
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

    parsed = json.loads(result["response"])

    return parsed["question"]


print("Current starting behaviour:")
print(customer_facts["starting_behaviour"])

print("\nNext information to collect:")
print(selected_information)

question = generate_question(selected_information)

print("\nAI question:")
print(question)