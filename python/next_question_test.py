from question_generation_test import generate_question
from question_selector_test import (
    find_missing_information,
    choose_next_question,
)

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

if __name__ == "__main__":


    missing_information = find_missing_information(
        customer_facts
    )

    next_information = choose_next_question(
        missing_information

    )

    next_question = generate_question(next_information)


    print("Current customer facts:")

    for key, value in customer_facts.items():
        print(f"{key}: {value}")


    print("\nMissing information:")

    for item in missing_information:
        print(f"- {item}")


    print("\nNext information to collect:")
    print(next_information)

    print("\nGenerated question:")
    print(next_question.question)   