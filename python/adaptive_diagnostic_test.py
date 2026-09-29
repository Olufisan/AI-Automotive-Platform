import json
import urllib.request

from pydantic import ValidationError

from diagnostic_schema import StartingBehaviourAnswer


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
}


customer_answer = "It turns over slowly."


priority = [
    "starting_behaviour",
    "frequency",
    "warning_lights",
]


def find_missing_information(facts):
    missing = []

    if not facts.get("starting_behaviour"):
        missing.append("starting_behaviour")

    if not facts.get("frequency"):
        missing.append("frequency")

    if not facts.get("warning_lights"):
        missing.append("warning_lights")

    return missing


def choose_next_information(missing):
    for item in priority:
        if item in missing:
            return item

    return None


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

If the selected information is "starting_behaviour",
ask whether the engine:
- turns over normally
- turns over slowly
- does not turn over at all

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


def extract_starting_behaviour(answer):
    prompt = f"""
Return JSON only.

Extract the customer's answer into the field
"starting_behaviour".

Do not diagnose the vehicle.

Do not add information.

Customer answer:

{answer}

Allowed values:

- turns over normally
- turns over slowly
- does not turn over at all
- unknown

Return exactly:

{{
    "starting_behaviour": "..."
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

    return json.loads(result["response"])


missing_information = find_missing_information(customer_facts)

print("Missing information:")
for item in missing_information:
    print(f"- {item}")


selected_information = choose_next_information(
    missing_information
)

print("\nNext information to collect:")
print(selected_information)


question = generate_question(selected_information)

print("\nAI question:")
print(question)


print("\nSimulated customer answer:")
print(customer_answer)


raw_answer = extract_starting_behaviour(customer_answer)

try:
    validated_answer = StartingBehaviourAnswer.model_validate(
        raw_answer
    )

    print("\nPydantic validation passed")

    print(validated_answer.model_dump_json(indent=2))

    customer_facts.update(
        validated_answer.model_dump()
    )

except ValidationError as error:
    print("\nPydantic validation failed")
    print(error)


customer_facts.update(
    validated_answer.model_dump()
)


print("\nUpdated customer facts:")
print(json.dumps(customer_facts, indent=2))


# Simulate the customer's answer to the frequency question.

frequency_answer = "It happens about once or twice a week."

print("\nSimulated frequency answer:")
print(frequency_answer)


frequency_prompt = f"""
Return JSON only.

You are extracting a structured fact from a customer's answer.

Extract ONLY the frequency of the starting problem.

Do not copy the full customer sentence.

Remove conversational wording such as:
- "It happens"
- "The problem happens"
- "I notice it"

Keep only the actual frequency.

Do not diagnose the vehicle.
Do not add information.
Do not guess.

Customer answer:

{frequency_answer}

For example:

Customer answer:
"It happens about once or twice a week."

Correct:
{{
    "frequency": "once or twice a week"
}}

Incorrect:
{{
    "frequency": "It happens about once or twice a week."
}}

Return exactly:

{{
    "frequency": "..."
}}
"""


payload = {
    "model": "qwen3:1.7b",
    "prompt": frequency_prompt,
    "stream": False,
    "think": False,
}


request = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
)


response = urllib.request.urlopen(
    request,
    timeout=60,
)


result = json.loads(
    response.read().decode()
)


frequency_data = json.loads(
    result["response"]
)


print("\nExtracted frequency:")
print(json.dumps(frequency_data, indent=2))


customer_facts.update(
    frequency_data
)


print("\nCustomer facts after frequency:")
print(json.dumps(customer_facts, indent=2))


remaining_information = find_missing_information(
    customer_facts
)

print("\nRemaining missing information:")

for item in remaining_information:
    print(f"- {item}")