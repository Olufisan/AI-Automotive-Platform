import os
from unittest.mock import MagicMock, patch

from automotive_evidence import AutomotiveEvidence
from database import save_evidence


def test_save_evidence():
    evidence = AutomotiveEvidence(
        evidence_type="customer_reported",
        observation="The grinding noise is mild.",
        context="",
        severity_or_intensity="mild",
        duration="",
        confirmed_by_technician=False,
    )

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (123,)

    mock_connection = MagicMock()
    mock_connection.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    with (
    patch.dict(
        os.environ,
        {
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_NAME": "test_db",
            "DB_USER": "test_user",
            "DB_PASSWORD": "test_password",
        },
    ),
    patch("database.psycopg.connect", return_value=mock_connection),
):
        record_id = save_evidence(
            "The grinding noise is mild.",
            evidence,
        )

    assert record_id == 123
    mock_cursor.execute.assert_called_once()
    mock_connection.commit.assert_called_once()