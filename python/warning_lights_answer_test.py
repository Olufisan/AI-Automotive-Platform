import json
import urllib.request

from pydantic import BaseModel, ValidationError


class WarningLightsAnswer(BaseModel):
    warning_lights: list[str]


customer_answer = "No, there are no warning lights."


def extract_warning_lights(answer):
    prompt = f"""
Return JSON only.

You are extracting a structured fact from a customer's answer.

Extract ONLY the warning lights mentioned by the customer.

Do not diagnose the vehicle.
Do not invent warning lights.
Do not add information that the customer did not provide.

If the customer says there are no warning lights,
return an empty list.

Customer answer:

{answer}

Return exactly:

{{
    "warning_lights": []
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

    response = urllib.request.urlopen(
        request,
        timeout=60,
    )

    result = json.loads(
        response.read().decode()
    )

    return json.loads(
        result["response"]
    )


print("Customer answer:")
print(customer_answer)

raw_answer = extract_warning_lights(
    customer_answer
)

print("\nRaw AI response:")
print(json.dumps(raw_answer, indent=2))


try:
    validated_answer = WarningLightsAnswer.model_validate(
        raw_answer
    )

    print("\nPydantic validation passed")

    print(
        validated_answer.model_dump_json(
            indent=2
        )
    )

except ValidationError as error:
    print("\nPydantic validation failed")
    print(error)