import json
import urllib.request

from pydantic import ValidationError
from diagnostic_schema import DiagnosticRecord


customer_message = """
My 2018 Volkswagen Golf sometimes struggles to start in the morning.
It usually happens when the engine is cold.
There are no warning lights on the dashboard.
"""


prompt = f"""
Return JSON only.

You are an information extraction system, NOT a diagnostic mechanic.

Extract ONLY facts explicitly stated by the customer.

NEVER:
- infer a diagnosis
- guess possible causes
- recommend tests
- recommend repairs
- add technical information
- invent missing information

Use exactly these fields:

vehicle:
  make
  model
  year

complaint
symptoms
warning_lights
conditions
possible_systems
possible_causes
missing_information
recommended_checks
confidence

Rules:
- Arrays must always be JSON arrays.
- If information is not explicitly provided, use an empty array.
- possible_causes MUST be an empty array.
- recommended_checks MUST be an empty array.
- confidence MUST be "Unknown / requires inspection".
- Do not diagnose the vehicle.

Customer message:
{customer_message}
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

raw_response = result["response"]

try:
    parsed_json = json.loads(raw_response)
    record = DiagnosticRecord.model_validate(parsed_json)

    print("Pydantic validation passed")
    print(record.model_dump_json(indent=2))

except json.JSONDecodeError as error:
    print("AI returned invalid JSON")
    print(error)

except ValidationError as error:
    print("Pydantic validation failed")
    print(error)