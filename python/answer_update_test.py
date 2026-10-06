from diagnostic_schema import DiagnosticAnswer


def update_customer_facts(
    customer_facts,
    answer: DiagnosticAnswer,
):
    updated_facts = customer_facts.copy()

    if answer.answer == "unknown":
        return updated_facts

    updated_facts[
        answer.information_type
    ] = answer.answer

    return updated_facts