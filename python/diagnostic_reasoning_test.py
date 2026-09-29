import json
import urllib.request

from pydantic import ValidationError

from diagnostic_schema import DiagnosticAnalysis


validated_facts = {
    "vehicle": {
        "make": "Volkswagen",
        "model": "Golf",
        "year": 2018,
    },
    "complaint": "Sometimes struggles to start in the morning.",
    "symptoms": [
        "struggles to start in the morning",
        "happens when the engine is cold",
    ],
    "warning_lights": [],
    "conditions": [],
}


prompt = f"""
Return JSON only.

You are a Virtual Senior Automotive Diagnostic Mechanic
with 15+ years of simulated diagnostic experience.

You are performing PRE-INSPECTION diagnostic reasoning.

The vehicle has NOT been physically inspected.

Use ONLY the information provided below.

Your job is to:
- identify possible vehicle systems
- identify possible causes
- explain evidence supporting each possibility
- identify evidence against possibilities when available
- identify missing information
- recommend appropriate diagnostic checks
- assign a cautious confidence level

IMPORTANT RULES:

- Do NOT claim that you physically inspected the vehicle.
- Do NOT claim that a physical fault is confirmed.
- Do NOT invent DTCs.
- Do NOT invent measurements.
- Do NOT invent service history.
- Do NOT invent vehicle specifications.
- Do NOT invent test results.
- Do NOT invent prices or repair costs.
- Do NOT recommend replacing a component as if the fault is confirmed.
- Physical inspection and diagnostic testing are required before confirming a fault.
- If evidence is insufficient, say so.
- Prefer "Possible" or "Unknown / requires inspection" when evidence is insufficient.
- Do not use "Confirmed" unless the supplied evidence explicitly supports a confirmed diagnosis.

Return exactly these fields:

possible_systems
possible_causes
evidence_for
evidence_against
missing_information
recommended_checks
confidence

All list fields must be JSON arrays.

Allowed confidence values:

"Confirmed"
"Highly likely"
"Possible"
"Unknown / requires inspection"

Validated customer facts:

{json.dumps(validated_facts, indent=2)}
"""


payload = {
    "model": "qwen3:4b-q4_K_M",
    "prompt": prompt,
    "stream": False,
    "think": False,
}


request = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
)


response = urllib.request.urlopen(request, timeout=120)
result = json.loads(response.read().decode())

raw_response = result["response"]

print("Raw AI response:")
print(raw_response)

try:
    parsed_json = json.loads(raw_response)
    analysis = DiagnosticAnalysis.model_validate(parsed_json)

    print("\nDiagnostic analysis validation passed")
    print(analysis.model_dump_json(indent=2))

except json.JSONDecodeError as error:
    print("\nAI returned invalid JSON")
    print(error)

except ValidationError as error:
    print("\nDiagnostic analysis validation failed")
    print(error)