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
    "conditions": [],
}


def find_missing_information(facts):
    missing = []

    if not facts.get("starting_behaviour"):
        missing.append("starting_behaviour")

    if not facts.get("frequency"):
        missing.append("frequency")

    if not facts.get("warning_lights"):
        missing.append("warning_lights")

    return missing


priority = [
    "starting_behaviour",
    "frequency",
    "warning_lights",
]


def choose_next_question(missing):
    for item in priority:
        if item in missing:
            return item

    return None


missing_information = find_missing_information(customer_facts)

next_question = choose_next_question(missing_information)


print("Missing information:")

for item in missing_information:
    print(f"- {item}")


print("\nNext information to collect:")

print(next_question)