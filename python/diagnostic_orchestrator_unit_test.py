from diagnostic_orchestrator import process_customer_answer


def test_process_customer_answer():
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

    result = process_customer_answer(
        customer_facts,
        "It happens once or twice a week.",
        "frequency",
    )

    assert result is not None
    assert result["answer"].information_type == "frequency"
    assert (
        result["updated_facts"]["frequency"]
        == "It happens once or twice a week."
    )
    assert result["next_information"] == "starting_behaviour"
    assert result["next_question"]


def test_process_customer_answer_does_not_modify_original_facts():
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

    process_customer_answer(
        customer_facts,
        "It happens once or twice a week.",
        "frequency",
    )

    assert "frequency" not in customer_facts

def test_process_customer_answer_returns_none_when_extraction_fails(
    monkeypatch,
):
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

    def fake_extract_answer(
        customer_answer,
        information_type,
    ):
        return None

    monkeypatch.setattr(
        "diagnostic_orchestrator.extract_answer",
        fake_extract_answer,
    )

    result = process_customer_answer(
        customer_facts,
        "unclear answer",
        "frequency",
    )

    assert result is None