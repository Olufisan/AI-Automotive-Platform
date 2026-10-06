from unittest.mock import patch

from next_question_test import (
    customer_facts,
    find_missing_information,
    choose_next_question,
    generate_question,
)


def test_next_question_is_generated_from_missing_information():

    missing_information = find_missing_information(
        customer_facts
    )

    next_information = choose_next_question(
        missing_information
    )

    with patch(
        "next_question_test.generate_question"
    ) as mock_generate_question:

        mock_generate_question.return_value.question = (
            "Are any warning lights showing on the dashboard?"
        )

        next_question = mock_generate_question(
            next_information
        )

        assert next_information == "warning_lights"

        assert next_question.question == (
            "Are any warning lights showing on the dashboard?"
        )

        mock_generate_question.assert_called_once_with(
            "warning_lights"
        )

def test_next_question_selects_starting_behaviour():

    facts = {
        "starting_behaviour": "",
        "frequency": "once or twice a week",
        "warning_lights": ["engine warning light"],
    }

    missing_information = find_missing_information(
        facts
    )

    next_information = choose_next_question(
        missing_information
    )

    assert next_information == "starting_behaviour"

def test_next_question_follows_priority_order():

    facts = {
        "starting_behaviour": "",
        "frequency": "",
        "warning_lights": [],
    }

    missing_information = find_missing_information(
        facts
    )

    next_information = choose_next_question(
        missing_information
    )

    assert missing_information == [
        "starting_behaviour",
        "frequency",
        "warning_lights",
    ]

    assert next_information == "starting_behaviour"