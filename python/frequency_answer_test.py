import json
import urllib.request

from pydantic import BaseModel, ValidationError


class FrequencyAnswer(BaseModel):
    frequency: str


customer_answer = "It happens about once or twice a week."


def extract_frequency(answer):
    prompt = f"""
Return JSON only.

You are extracting information from a customer's answer.

Extract ONLY how often the starting problem occurs.

Do not diagnose the vehicle.
Do not add information.
Do not guess.

Customer answer:

{answer}

Return exactly:

{{
    "frequency": "..."
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


print("Customer answer:")
print(customer_answer)

raw_answer = extract_frequency(customer_answer)

print("\nRaw AI response:")
print(json.dumps(raw_answer, indent=2))

try:
    validated_answer = FrequencyAnswer.model_validate(
        raw_answer
    )

    print("\nPydantic validation passed")

    print(validated_answer.model_dump_json(indent=2))

except ValidationError as error:
    print("\nPydantic validation failed")
    print(error)