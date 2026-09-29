from diagnostic_schema import WorkshopDiagnosticReport


report = WorkshopDiagnosticReport(
    vehicle={
        "make": "Volkswagen",
        "model": "Golf",
        "year": 2018,
    },
    customer_complaint=(
        "The vehicle is difficult to start after "
        "driving for about 30 minutes."
    ),
    evidence=[
        {
            "source": "customer_reported",
            "information": "The engine turns over slowly.",
        }
    ],
    technician_evidence=[
        {
            "observation": "Battery terminals show visible corrosion.",
        }
    ],
    diagnostic_tests=[
        {
            "test_name": "Battery test",
            "result": "Reduced starting capacity.",
        }
    ],

        reasoning_links=[
        {
            "evidence_source": "customer_reported",
            "evidence_information": "The engine turns over slowly.",
            "reasoning": (
                "This makes the starting system relevant "
                "for further investigation."
            ),
        }
    ],
    key_observations=[
        "The engine turns over slowly.",
        "The problem occurs after approximately 30 minutes of driving.",
    ],
    possible_systems=[
        "Electrical system",
        "Starting system",
    ],
    possible_causes=[
        "Battery-related issue",
        "Electrical connection issue",
        "Starter circuit issue",
    ],
    reasons_to_consider=[
        "The engine turns over slowly.",
        "Starting-system evidence requires further investigation.",
    ],
    missing_information=[
        "Further diagnostic testing is required.",
    ],
    recommended_checks=[
        "Inspect the battery and electrical connections.",
        "Test the starting circuit.",
    ],
    confidence="Unknown / requires inspection",
)


print("Workshop report created successfully")
print()
print(report.model_dump_json(indent=2))