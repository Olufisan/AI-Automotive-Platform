import json
import urllib.request

from pydantic import ValidationError

from diagnostic_schema import StartingBehaviourAnswer


customer_answer = "It turns over slowly."


prompt = f"""
Return JSON only.

You are an information extraction assistant.

Extract the customer's answer into the specified field.

Do not diagnose the vehicle.

Do not suggest a repair.

Do not add information that the customer did not provide.

The information being collected is:

starting_behaviour

The customer's answer is:

{customer_answer}

Return exactly this JSON structure:

{{
    "starting_behaviour": "..."
}}

Use one of these values when supported by the customer's answer:

- turns over normally
- turns over slowly
- does not turn over at all

If the answer does not clearly provide the information,
return:

"unknown"
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


try:
    parsed_json = json.loads(result["response"])

    answer = StartingBehaviourAnswer.model_validate(parsed_json)

    print("\nPydantic validation passed")
    print(answer.model_dump_json(indent=2))

except json.JSONDecodeError as error:
    print("\nAI returned invalid JSON")
    print(error)

except ValidationError as error:
    print("\nPydantic validation failed")
    print(error)