from pydantic import ValidationError

from diagnostic_schema import DiagnosticRecord


test_data = {
    "vehicle": {
        "make": "Volkswagen",
        "model": "Golf",
        "year": 1800
    },
    "complaint": "Vehicle struggles to start.",
    "symptoms": [],
    "warning_lights": [],
    "conditions": [],
    "possible_systems": [],
    "possible_causes": [],
    "missing_information": [],
    "recommended_checks": [],
    "confidence": "Unknown / requires inspection"
}


try:
    record = DiagnosticRecord.model_validate(test_data)

    print("Validation unexpectedly passed")
    print(record.model_dump_json(indent=2))

except ValidationError as error:
    print("Validation correctly rejected the invalid data")
    print(error)