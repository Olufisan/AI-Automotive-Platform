import os
from unittest.mock import MagicMock, patch

from automotive_evidence import AutomotiveEvidence
from database import check_database_connection, save_evidence


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

def test_check_database_connection():
    mock_cursor = MagicMock()

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
        result = check_database_connection()

    assert result is True
    mock_cursor.execute.assert_called_once_with("SELECT 1")

def test_save_evidence_passes_correct_values_to_database():
    evidence = AutomotiveEvidence(
        evidence_type="customer_reported",
        observation="The grinding noise is mild.",
        context="",
        severity_or_intensity="mild",
        duration="three days",
        confirmed_by_technician=False,
    )

    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (456,)

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

    assert record_id == 456

    executed_sql, executed_values = mock_cursor.execute.call_args.args

    assert "INSERT INTO automotive_evidence" in executed_sql
    assert executed_values == (
        "The grinding noise is mild.",
        "The grinding noise is mild.",
        "",
        "mild",
        "three days",
        False,
    )