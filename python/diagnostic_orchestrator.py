from answer_extraction_test import extract_answer
from answer_update_test import update_customer_facts
from question_generation_test import generate_question
from question_selector_test import (
    find_missing_information,
    choose_next_question,
)


def process_customer_answer(
    customer_facts,
    customer_answer,
    information_type,
):
    answer = extract_answer(
        customer_answer,
        information_type,
    )

    if answer is None:
        return None

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

    if next_information is None:
        return {
            "answer": answer,
            "updated_facts": updated_facts,
            "next_information": None,
            "next_question": None,
        }

    next_question = generate_question(
        next_information,
    )

    return {
        "answer": answer,
        "updated_facts": updated_facts,
        "next_information": next_information,
        "next_question": next_question.question,
    }

