from fastapi.testclient import TestClient

from api import app


client = TestClient(app)


def test_process_diagnostic_endpoint():
    response = client.post(
        "/process-diagnostic",
        json={
            "customer_facts": {
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
                "conditions": [],
            },
            "customer_answer": (
                "It happens once or twice a week."
            ),
            "information_type": "frequency",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["request_id"]
    assert data["processing_time_seconds"] is not None
    assert data["result"]["updated_facts"]["frequency"] == (
        "It happens once or twice a week."
    )
    assert data["result"]["next_information"] == (
        "starting_behaviour"
    )
    assert data["result"]["next_question"] is not None

def test_process_diagnostic_endpoint_handles_failure(monkeypatch):
    def fake_process_customer_answer(
        customer_facts,
        customer_answer,
        information_type,
    ):
        return None

    monkeypatch.setattr(
        "api.process_customer_answer",
        fake_process_customer_answer,
    )

    response = client.post(
        "/process-diagnostic",
        json={
            "customer_facts": {},
            "customer_answer": "I don't know.",
            "information_type": "frequency",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is False
    assert data["request_id"]
    assert data["processing_time_seconds"] is not None
    assert data["error_code"] == (
        "DIAGNOSTIC_PROCESSING_FAILED"
    )