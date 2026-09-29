from unittest.mock import patch
from fastapi.testclient import TestClient
from api import app
from automotive_evidence import AutomotiveEvidence
client = TestClient(app)
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "AI Automotive Platform",
    }
def test_extract_evidence():
    with patch("api.save_evidence", return_value=999):
        response = client.post(
            "/extract-evidence",
            json={
                "customer_message": "The brake pedal feels soft.",
            },
        )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["record_id"] == 999
    assert "evidence" in data
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "record_id" in data
    assert "evidence" in data
def test_extract_evidence_rejects_non_string_message():
    response = client.post(
        "/extract-evidence",
        json={
            "customer_message": 12345,
        },
    )
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
    assert data["record_id"] == 1000
    assert data["evidence"]["observation"] == (
        "The brake pedal feels soft.")
