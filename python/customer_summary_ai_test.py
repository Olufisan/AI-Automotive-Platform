import json
import urllib.request

from diagnostic_schema import CustomerDiagnosticSummary


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
    "starting_behaviour": "turns over slowly",
    "frequency": "once or twice a week",
    "warning_lights": [],
}


prompt = f"""
Return JSON only.

You are a customer communication assistant for an automotive
workshop.

Your job is to write a short, clear customer-facing summary
based ONLY on the supplied customer information.

The vehicle has NOT been physically inspected.

Do not diagnose the vehicle.

Do not suggest that a component has failed.

Do not mention possible causes or internal diagnostic reasoning.

Do not invent:
- faults
- DTCs
- measurements
- test results
- service history
- prices
- repair costs
- repair recommendations

The customer should understand:

1. What information has been collected.
2. That the vehicle has not yet been physically inspected.
3. That the cause cannot currently be confirmed.
4. What the next step is.

Use simple language suitable for a normal vehicle owner.

Do not use technical language unless necessary.

The summary should be reassuring but must not falsely promise
that the vehicle will be repaired or that a particular fault
will be found.

Customer information:

{json.dumps(customer_facts, indent=2)}

Return exactly this JSON structure:

{{
    "summary": "",
    "inspection_required": true,
    "next_step": ""
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


print("Sending customer information to Qwen3 1.7B...")

response = urllib.request.urlopen(
    request,
    timeout=60,
)


result = json.loads(
    response.read().decode()
)


print("\nRaw AI response:")

print(result["response"])


parsed_json = json.loads(
    result["response"]
)


try:
    summary = CustomerDiagnosticSummary.model_validate(
        parsed_json
    )

    print("\nPydantic validation passed")

    print(
        summary.model_dump_json(
            indent=2
        )
    )

except Exception as error:
    print("\nCustomer summary validation failed")

    print(error)