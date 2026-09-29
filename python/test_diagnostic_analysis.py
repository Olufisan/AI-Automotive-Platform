from pydantic import ValidationError

from diagnostic_schema import DiagnosticAnalysis


test_data = {
    "possible_systems": ["Starting system"],
    "possible_causes": ["Battery-related issue"],
    "evidence_for": ["Vehicle struggles to start when cold"],
    "evidence_against": [],
    "missing_information": ["Battery condition is unknown"],
    "recommended_checks": ["Check battery condition"],
    "confidence": "Certain",
}


try:
    analysis = DiagnosticAnalysis.model_validate(test_data)

    print("Validation unexpectedly passed")
    print(analysis.model_dump_json(indent=2))

except ValidationError as error:
    print("Diagnostic analysis validation correctly rejected the invalid data")
    print(error)