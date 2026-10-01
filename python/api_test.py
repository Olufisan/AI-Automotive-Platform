from unittest.mock import patch

from fastapi.testclient import TestClient

from api import app
from automotive_evidence import AutomotiveEvidence


client = TestClient(app)


def test_health_check():
    with patch("api.check_database_connection", return_value=True):
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "AI Automotive Platform",
        "database": "available",
        "version": "1.0.0",
    }


def test_health_check_handles_database_failure():
    with patch(
        "api.check_database_connection",
        side_effect=Exception("Database connection failed"),
    ):
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "unhealthy",
        "service": "AI Automotive Platform",
        "database": "unavailable",
    }


def test_extract_evidence():
    fake_evidence = AutomotiveEvidence(
        evidence_type="customer_reported",
        observation="The brake pedal feels soft.",
        context="",
        severity_or_intensity="not specified",
        duration="",
        confirmed_by_technician=False,
    )

    with (
        patch("api.extract_evidence", return_value=fake_evidence),
        patch("api.save_evidence", return_value=999),
    ):
        response = client.post(
            "/extract-evidence",
            json={
                "customer_message": "The brake pedal feels soft.",
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["request_id"]
    assert data["record_id"] == 999
    assert data["evidence"]["observation"] == (
        "The brake pedal feels soft."
    )


def test_extract_evidence_rejects_non_string_message():
    response = client.post(
        "/extract-evidence",
        json={
            "customer_message": 12345,
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["request_id"]
    assert data["detail"]

    assert response.status_code == 422


def test_extract_evidence_with_mocked_dependencies():
    fake_evidence = AutomotiveEvidence(
        evidence_type="customer_reported",
        observation="The brake pedal feels soft.",
        context="",
        severity_or_intensity="not specified",
        duration="",
        confirmed_by_technician=False,
    )

    with (
        patch("api.extract_evidence", return_value=fake_evidence),
        patch("api.save_evidence", return_value=1000),
    ):
        response = client.post(
            "/extract-evidence",
            json={
                "customer_message": "The brake pedal feels soft.",
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["request_id"]
    assert data["record_id"] == 1000
    assert data["evidence"]["observation"] == (
        "The brake pedal feels soft."
    )


def test_extract_evidence_handles_ai_failure():
    with patch("api.extract_evidence", return_value=None):
        response = client.post(
            "/extract-evidence",
            json={
                "customer_message": (
                    "The engine is making a strange noise."
                ),
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is False
    assert data["request_id"]
    assert data["record_id"] is None
    assert data["evidence"] is None
    assert data["message"] == "Evidence extraction failed safely."


def test_extract_evidence_handles_database_failure():
    mock_evidence = AutomotiveEvidence(
        evidence_type="customer_reported",
        observation="The engine is making a strange noise.",
        context="",
        severity_or_intensity="not specified",
        duration="",
        confirmed_by_technician=False,
    )

    with (
        patch("api.extract_evidence", return_value=mock_evidence),
        patch(
            "api.save_evidence",
            side_effect=Exception("Database connection failed"),
        ),
    ):
        response = client.post(
            "/extract-evidence",
            json={
                "customer_message": (
                    "The engine is making a strange noise."
                ),
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is False
    assert data["request_id"]
    assert data["record_id"] is None
    assert data["evidence"] is None
    assert data["message"] == "Evidence could not be saved."


def test_extract_evidence_rejects_message_over_2000_characters():
    response = client.post(
        "/extract-evidence",
        json={
            "customer_message": "A" * 2001,
        },
    )

    assert response.status_code == 422


def test_extract_evidence_accepts_message_at_2000_characters():
    with patch("api.extract_evidence", return_value=None):
        response = client.post(
            "/extract-evidence",
            json={
                "customer_message": "A" * 2000,
            },
        )

    assert response.status_code == 200