from question_selector_test import (
    choose_next_question,
    find_missing_information,
)


def test_find_missing_information():
    facts = {
        "vehicle": {
            "make": "Volkswagen",
            "model": "Golf",
            "year": 2018,
        },
        "complaint": "The vehicle is difficult to start.",
        "starting_behaviour": "",
        "frequency": "",
        "warning_lights": "",
    }

    missing = find_missing_information(facts)

    assert missing == [
        "starting_behaviour",
        "frequency",
        "warning_lights",
    ]


def test_choose_next_question():
    missing = [
        "starting_behaviour",
        "frequency",
        "warning_lights",
    ]

    result = choose_next_question(missing)

    assert result == "starting_behaviour"

def test_choose_next_question_returns_none_when_nothing_is_missing():
    result = choose_next_question([])

    assert result is None