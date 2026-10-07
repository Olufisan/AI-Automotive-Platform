import httpx
import psycopg


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

    record_id = data["record_id"]

    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="automotive",
        user="n8n",
        password="n8npassword",
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    customer_message,
                    observation,
                    context,
                    severity_or_intensity,
                    duration,
                    confirmed_by_technician
                FROM automotive_evidence
                WHERE id = %s
                """,
                (record_id,),
            )

            record = cursor.fetchone()

    assert record is not None
    assert record[0] == record_id
    assert record[1] == (
        "The steering wheel shakes when I drive above 60 mph "
        "and it started yesterday."
    )
    assert record[3] == ""
    assert record[4] == "not specified"
    assert record[5] == "yesterday"
    assert record[6] is False

    evidence = data["evidence"]

    assert evidence["evidence_type"] == "customer_reported"
    assert evidence["observation"]
    assert evidence["severity_or_intensity"] == "not specified"
    assert evidence["duration"] == "yesterday"
    assert evidence["confirmed_by_technician"] is False