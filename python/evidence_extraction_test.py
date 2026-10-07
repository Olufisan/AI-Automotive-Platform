import json
import urllib.error
from unittest.mock import patch

from evidence_extraction import extract_evidence


def test_extract_evidence_success():
    mock_response = {
        "response": json.dumps(
            {
                "observation": "The grinding noise is mild.",
                "context": "",
                "duration": "",
                "confirmed_by_technician": False,
            }
        )
    }

    with patch(
        "evidence_extraction.urllib.request.urlopen"
    ) as mock_urlopen:
        mock_urlopen.return_value.read.return_value = json.dumps(
            mock_response
        ).encode()

        result = extract_evidence(
            "The grinding noise is mild.",
            max_attempts=2,
        )

    assert result is not None
    assert result.evidence_type == "customer_reported"
    assert result.observation == "The grinding noise is mild."
    assert result.severity_or_intensity == "mild"
    assert result.confirmed_by_technician is False


def test_extract_evidence_rejects_inferred_technician_confirmation():
    mock_response = {
        "response": json.dumps(
            {
                "observation": "The grinding noise is mild.",
                "context": "",
                "duration": "",
                "confirmed_by_technician": True,
            }
        )
    }

    with patch(
        "evidence_extraction.urllib.request.urlopen"
    ) as mock_urlopen:
        mock_urlopen.return_value.read.return_value = json.dumps(
            mock_response
        ).encode()

        result = extract_evidence(
            "The grinding noise is mild.",
            max_attempts=1,
        )

        assert result is None

def test_extract_evidence_rejects_inferred_severity():
    mock_response = {
        "response": json.dumps(
            {
                "observation": (
                    "My car makes a grinding noise when I brake."
                ),
                "context": "",
                "duration": "",
                "confirmed_by_technician": False,
            }
        )
    }

    with patch(
        "evidence_extraction.urllib.request.urlopen"
    ) as mock_urlopen:
        mock_urlopen.return_value.read.return_value = json.dumps(
            mock_response
        ).encode()

        result = extract_evidence(
            "My car makes a grinding noise when I brake.",
            max_attempts=1,
        )

    assert result is not None
    assert result.severity_or_intensity == "not specified"


def test_extract_evidence_accepts_explicit_technician_confirmation():
    mock_response = {
        "response": json.dumps(
            {
                "observation": (
                    "The grinding noise happens when I brake."
                ),
                "context": (
                    "A technician checked it yesterday and confirmed "
                    "the grinding noise."
                ),
                "duration": "yesterday",
                "confirmed_by_technician": True,
            }
        )
    }

    with patch(
        "evidence_extraction.urllib.request.urlopen"
    ) as mock_urlopen:
        mock_urlopen.return_value.read.return_value = json.dumps(
            mock_response
        ).encode()

        result = extract_evidence(
            (
                "The grinding noise happens when I brake. "
                "A technician checked it yesterday and confirmed "
                "the grinding noise."
            ),
            max_attempts=1,
        )

    assert result is not None
    assert result.confirmed_by_technician is True
    assert result.duration == "yesterday"


def test_extract_evidence_rejects_invalid_duration():
    mock_response = {
        "response": json.dumps(
            {
                "observation": "The brake pedal feels soft.",
                "context": "",
                "duration": "very serious",
                "confirmed_by_technician": False,
            }
        )
    }

    with patch(
        "evidence_extraction.urllib.request.urlopen"
    ) as mock_urlopen:
        mock_urlopen.return_value.read.return_value = json.dumps(
            mock_response
        ).encode()

        result = extract_evidence(
            "The brake pedal feels soft.",
            max_attempts=1,
        )

    assert result is not None
    assert result.duration == ""


def test_extract_evidence_preserves_context():
    mock_response = {
        "response": json.dumps(
            {
                "observation": (
                    "My car makes a grinding noise when I brake hard."
                ),
                "context": "when I brake hard",
                "duration": "",
                "confirmed_by_technician": False,
            }
        )
    }

    with patch(
        "evidence_extraction.urllib.request.urlopen"
    ) as mock_urlopen:
        mock_urlopen.return_value.read.return_value = json.dumps(
            mock_response
        ).encode()

        result = extract_evidence(
            "My car makes a grinding noise when I brake hard.",
            max_attempts=1,
        )

    assert result is not None
    assert result.context == "when I brake hard"
    

def test_extract_evidence_returns_empty_duration_when_not_stated():
    mock_response = {
        "response": json.dumps(
            {
                "observation": "The brake pedal feels soft.",
                "context": "",
                "duration": "",
                "confirmed_by_technician": False,
            }
        )
    }

    with patch(
        "evidence_extraction.urllib.request.urlopen"
    ) as mock_urlopen:
        mock_urlopen.return_value.read.return_value = json.dumps(
            mock_response
        ).encode()

        result = extract_evidence(
            "The brake pedal feels soft.",
            max_attempts=1,
        )

    assert result is not None
    assert result.duration == ""


def test_extract_evidence_handles_connection_error():
    with patch(
        "evidence_extraction.urllib.request.urlopen",
        side_effect=urllib.error.URLError("Ollama unavailable"),
    ):
        result = extract_evidence(
            "The brake pedal feels soft.",
            max_attempts=1,
        )

    assert result is None


def test_extract_evidence_handles_missing_ai_response():
    mock_response = {}

    with patch(
        "evidence_extraction.urllib.request.urlopen"
    ) as mock_urlopen:
        mock_urlopen.return_value.read.return_value = json.dumps(
            mock_response
        ).encode()

        result = extract_evidence(
            "The brake pedal feels soft.",
            max_attempts=1,
        )

    assert result is None