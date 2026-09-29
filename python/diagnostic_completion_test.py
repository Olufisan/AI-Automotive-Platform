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
    "symptoms": [],
    "warning_lights": [],
    "starting_behaviour": "turns over slowly",
    "frequency": "once or twice a week",
}


priority = [
    "starting_behaviour",
    "frequency",
    "warning_lights",
]


def find_missing_information(facts):
    missing = []

    if not facts.get("starting_behaviour"):
        missing.append("starting_behaviour")

    if not facts.get("frequency"):
        missing.append("frequency")

    if "warning_lights" not in facts:
        missing.append("warning_lights")

    return missing


def choose_next_information(missing):
    for item in priority:
        if item in missing:
            return item

    return None


missing_information = find_missing_information(
    customer_facts
)

next_information = choose_next_information(
    missing_information
)


print("Missing information:")

if missing_information:
    for item in missing_information:
        print(f"- {item}")
else:
    print("None")


print("\nNext information to collect:")
print(next_information)


if next_information is None:
    print("\nDiagnostic information collection is complete.")