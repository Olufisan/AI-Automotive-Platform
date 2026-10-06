import httpx


def test_real_extract_evidence():
    response = httpx.post(
        "http://127.0.0.1:8000/extract-evidence",
        json={
            "customer_message": (
                "The steering wheel shakes when I drive above 60 mph "
                "and it started yesterday."
            )
        },
        timeout=60,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["record_id"] is not None
    assert data["evidence"] is not None

    evidence = data["evidence"]

    assert evidence["evidence_type"] == "customer_reported"
    assert evidence["observation"]
    assert evidence["severity_or_intensity"] == "not specified"
    assert evidence["duration"] == "yesterday"
    assert evidence["confirmed_by_technician"] is False