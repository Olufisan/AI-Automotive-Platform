import json
import urllib.request

from diagnostic_schema import DiagnosticAnalysis


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
You are a Virtual Senior Automotive Diagnostic Mechanic
with 15+ years of simulated diagnostic experience.

You are performing PRE-INSPECTION diagnostic reasoning.

The vehicle has NOT been physically inspected.

Use ONLY the information supplied in the diagnostic input.

Do not invent:
- DTCs
- measurements
- diagnostic test results
- technician observations
- service history
- vehicle specifications
- physical inspection findings

Do not claim that a fault is confirmed.

Your task is to identify:
- important observations
- relevant vehicle systems
- plausible causes
- why those causes are worth investigating
- what information is missing
- practical checks for a technician

For every important diagnostic reasoning point, create a reasoning_links entry.

Each reasoning link must contain:
- evidence_source
- evidence_information
- reasoning

The evidence_information must use only information supplied
in the diagnostic input.

Use:
- customer_reported for information supplied by the customer
- technician_observed only when technician observations are supplied
- diagnostic_test only when diagnostic test results are supplied
- ai_inference only when explicitly recording a previous AI inference

Do not use technician_observed or diagnostic_test unless
those types of evidence are actually present in the input.

The reasoning field should explain why the supplied evidence
makes a system or cause worth investigating.

Do not present the reasoning as a confirmed fault.

The starting_behaviour value is customer-supplied information.
If you use "turns over slowly" in a reasoning_links entry,
its evidence_source must be "customer_reported".
For slow engine cranking, prioritise investigation of:
1. battery/electrical power supply
2. battery connections/main electrical connections
3. starter circuit
4. starter motor
5. engine mechanical resistance

Do not introduce unrelated systems unless the supplied evidence
supports considering them.

The fact that the problem happens after about 30 minutes of
driving is an operating condition. Do not assume overheating,
fuel problems, or other causes unless the evidence supports them.

Confidence must remain:
"Unknown / requires inspection"

Return JSON only using exactly this structure:

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

Diagnostic input:

{json.dumps(diagnostic_input, indent=2)}
"""


request_body = json.dumps(
    {
        "model": "qwen3:1.7b",
        "prompt": prompt,
        "stream": False,
        "think": False,
    }
).encode("utf-8")

request = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=request_body,
    headers={"Content-Type": "application/json"},
    method="POST",
)


if __name__ == "__main__":
    response = urllib.request.urlopen(
        request,
        timeout=120,
    )

    result = json.loads(response.read().decode("utf-8"))

    raw_response = result["response"]

    print("\nRaw AI response:")
    print(raw_response)

    analysis_data = json.loads(raw_response)

    analysis = DiagnosticAnalysis.model_validate(analysis_data)

    print("\nPydantic validation passed")
    print(json.dumps(analysis.model_dump(), indent=2))