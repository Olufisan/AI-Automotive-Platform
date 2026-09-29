import json
import urllib.request

from diagnostic_schema import (
    DiagnosticAnalysis,
    WorkshopDiagnosticReport,
)


diagnostic_input = {
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
    "frequency": "once or twice a week",
}


prompt = f"""
Return JSON only.

You are a Virtual Senior Automotive Diagnostic Mechanic
with simulated diagnostic experience.

You are performing PRE-INSPECTION diagnostic reasoning.

You have NOT physically inspected the vehicle.

Use ONLY the evidence provided below.

Do not invent:
- DTCs
- measurements
- test results
- service history
- vehicle specifications
- physical inspection findings

Do not claim that a fault is confirmed.

Your task is to perform structured pre-inspection reasoning.

Follow this order:

1. Identify the most important observed symptom.
2. Identify systems directly relevant to that symptom.
3. Identify possible causes within those systems.
4. Only describe something as evidence if it is actually present
   in the supplied customer information.
5. Do not treat the absence of information as evidence against
   a fault.
6. Clearly distinguish:
   - observed evidence
   - possible explanation
   - missing evidence
7. Recommend checks that would distinguish between the
   important possibilities.

Diagnostic reasoning rule:

If the customer reports that the engine turns over slowly,
prioritise causes that can directly affect engine cranking speed.

When the reported symptom is "the engine turns over slowly",
use this diagnostic relevance order:

1. Battery and electrical power supply
2. Battery connections and main electrical connections
3. Starter circuit
4. Starter motor
5. Engine mechanical resistance

Only consider fuel delivery, ignition, cooling, overheating,
or other systems if the supplied customer information contains
a specific symptom that points toward them.

Do not introduce a system merely because it can theoretically
cause a starting problem.

For every possible cause, ask:

"Is there something in the supplied information that makes
this cause relevant?"

If the answer is no, do not include that cause.

Do not use generic automotive knowledge as a reason to add
extra possible causes.

For example:

Bad reasoning:
"The vehicle has a starting problem, therefore fuel pump
failure is a possible cause."

Better reasoning:
"The engine turns over slowly, therefore the battery,
electrical supply, starter circuit, or starter motor should
be investigated."

The fact that the problem happens after approximately
30 minutes of driving is an operating condition that requires
further investigation. It is NOT evidence that the vehicle
is overheating and it is NOT evidence of a fuel-system fault.

Do not assume that a warm engine means overheating.

Do not assume that a starting problem is a fuel problem.

Do not assume that a starting problem is an ignition problem.

The purpose of this stage is to help a technician decide
what evidence to collect during physical inspection.
It is NOT to determine the final fault remotely.

Important:
The complaint says the vehicle is difficult to start
after driving for about 30 minutes.

The customer reported that the engine turns over slowly.

Do not reinterpret "about 30 minutes" as a weather condition.

Because there has been no physical inspection,
confidence must remain:

"Unknown / requires inspection"

Diagnostic evidence:

For every important diagnostic reasoning point, create a reasoning_links entry.

Each reasoning link must contain:
- evidence_source
- evidence_information
- reasoning

The evidence_information must use only information supplied in the diagnostic input.

Do not invent or rewrite evidence.

Use:
- customer_reported for information supplied by the customer
- technician_observed only when technician observations are supplied
- diagnostic_test only when diagnostic test results are supplied
- ai_inference only when explicitly recording a previous AI inference

Do not use technician_observed or diagnostic_test unless those types of evidence are actually present in the input.

The reasoning field should explain why the supplied evidence makes a system or cause worth investigating.

Do not present the reasoning as a confirmed fault.

{json.dumps(diagnostic_input, indent=2)}

Return exactly this JSON structure:

{{
    "reasoning_links": [],
    "key_observations": [],
    "possible_systems": [],
    "possible_causes": [],
    "reasons_to_consider": [],
     "missing_information": [],
    "recommended_checks": [],
    "confidence": "Unknown / requires inspection"
}}
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


print("Sending diagnostic evidence to Qwen3 4B...")

response = urllib.request.urlopen(
    request,
    timeout=300,
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
    analysis = DiagnosticAnalysis.model_validate(
        parsed_json
    )

    print("\nPydantic validation passed")

    print(
        analysis.model_dump_json(
            indent=2
        )
    )

    workshop_report = WorkshopDiagnosticReport(
        vehicle=diagnostic_input["vehicle"],
        customer_complaint=diagnostic_input["complaint"],
        reasoning_links=analysis.reasoning_links,
        key_observations=analysis.key_observations,
        possible_systems=analysis.possible_systems,
        possible_causes=analysis.possible_causes,
        reasons_to_consider=analysis.reasons_to_consider,
        missing_information=analysis.missing_information,
        recommended_checks=analysis.recommended_checks,
        confidence=analysis.confidence,
        physical_inspection_required=True,
    )

    print("\nWorkshop report created successfully")

    print(
        workshop_report.model_dump_json(
            indent=2
        )
    )

except Exception as error:
    print("\nValidation or workshop report creation failed")

    print(error)