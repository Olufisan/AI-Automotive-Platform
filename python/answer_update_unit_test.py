from diagnostic_schema import DiagnosticAnswer
from answer_update_test import update_customer_facts
from answer_extraction_test import extract_answer
from question_generation_test import generate_question
from question_selector_test import (
    find_missing_information,
    choose_next_question,
)


def test_update_customer_facts():

    customer_facts = {
        "vehicle": {
            "make": "Volkswagen",
            "model": "Golf",
            "year": 2018,
        },
        "complaint": (
            "The vehicle is difficult to start "
            "after driving for about 30 minutes."
        ),
        "symptoms": [],
        "warning_lights": [],
    }

    answer = DiagnosticAnswer(
        information_type="frequency",
        answer="once or twice a week",
    )

    updated_facts = update_customer_facts(
        customer_facts,
        answer,
    )

    assert updated_facts["frequency"] == (
        "once or twice a week"
    )

def test_update_starting_behaviour():

    customer_facts = {
        "vehicle": {
            "make": "Volkswagen",
            "model": "Golf",
            "year": 2018,
        },
        "complaint": (
            "The vehicle is difficult to start "
            "after driving for about 30 minutes."
        ),
        "symptoms": [],
        "warning_lights": [],
    }

    answer = DiagnosticAnswer(
        information_type="starting_behaviour",
        answer="turns over slowly",
    )

    updated_facts = update_customer_facts(
        customer_facts,
        answer,
    )

    assert updated_facts["starting_behaviour"] == (
        "turns over slowly"
    )

def test_unknown_answer_does_not_update_facts():

    customer_facts = {
        "vehicle": {
            "make": "Volkswagen",
            "model": "Golf",
            "year": 2018,
        },
        "complaint": (
            "The vehicle is difficult to start "
            "after driving for about 30 minutes."
        ),
        "symptoms": [],
        "warning_lights": [],
    }

    answer = DiagnosticAnswer(
        information_type="frequency",
        answer="unknown",
    )

    updated_facts = update_customer_facts(
        customer_facts,
        answer,
    )

    assert "frequency" not in updated_facts

def test_original_customer_facts_are_not_modified():

    customer_facts = {
        "vehicle": {
            "make": "Volkswagen",
            "model": "Golf",
            "year": 2018,
        },
        "complaint": (
            "The vehicle is difficult to start "
            "after driving for about 30 minutes."
        ),
        "symptoms": [],
        "warning_lights": [],
    }

    answer = DiagnosticAnswer(
        information_type="frequency",
        answer="once or twice a week",
    )

    updated_facts = update_customer_facts(
        customer_facts,
        answer,
    )

    assert "frequency" not in customer_facts

    assert updated_facts["frequency"] == (
        "once or twice a week"
    )

    


def test_updated_facts_can_be_used_by_question_selector():

    customer_facts = {
        "vehicle": {
            "make": "Volkswagen",
            "model": "Golf",
            "year": 2018,
        },
        "complaint": (
            "The vehicle is difficult to start "
            "after driving for about 30 minutes."
        ),
        "symptoms": [],
        "warning_lights": [],
    }

    answer = DiagnosticAnswer(
        information_type="frequency",
        answer="once or twice a week",
    )

    updated_facts = update_customer_facts(
        customer_facts,
        answer,
    )

    missing_information = find_missing_information(
        updated_facts
    )

    assert "frequency" not in missing_information
    assert "starting_behaviour" in missing_information
    assert "warning_lights" in missing_information

def test_updated_facts_choose_next_question():
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
    }

    answer = DiagnosticAnswer(
        information_type="frequency",
        answer="once or twice a week",
    )

    updated_facts = update_customer_facts(
        customer_facts,
        answer,
    )

    missing_information = find_missing_information(
        updated_facts
    )

    next_question = choose_next_question(
        missing_information
    )

    assert next_question == "starting_behaviour"

def test_ai_answer_can_update_customer_facts():
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
    }

    customer_answer = "It happens once or twice a week."

    answer = extract_answer(
        customer_answer,
        "frequency",
    )

    assert answer is not None
    assert answer.information_type == "frequency"

    updated_facts = update_customer_facts(
        customer_facts,
        answer,
    )

    assert updated_facts["frequency"] == "It happens once or twice a week."

def test_ai_answer_updates_facts_and_selects_next_question():
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
    }

    customer_answer = "It happens once or twice a week."

    answer = extract_answer(
        customer_answer,
        "frequency",
    )

    assert answer is not None

    updated_facts = update_customer_facts(
        customer_facts,
        answer,
    )

    missing_information = find_missing_information(
        updated_facts
    )

    next_information = choose_next_question(
        missing_information
    )

    assert "frequency" not in missing_information
    assert next_information == "starting_behaviour"

def test_ai_answer_flow_generates_next_question():
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
    }

    customer_answer = "It happens once or twice a week."

    answer = extract_answer(
        customer_answer,
        "frequency",
    )

    assert answer is not None

    updated_facts = update_customer_facts(
        customer_facts,
        answer,
    )

    missing_information = find_missing_information(
        updated_facts,
    )

    next_information = choose_next_question(
        missing_information,
    )

    next_question = generate_question(
        next_information,
    )

    assert next_information == "starting_behaviour"
    assert next_question.question