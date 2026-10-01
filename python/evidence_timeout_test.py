from unittest.mock import patch

from evidence_extraction_test import extract_evidence


def test_extract_evidence_handles_timeout():
    with patch(
        "evidence_extraction_test.urllib.request.urlopen",
        side_effect=TimeoutError,
    ):
        result = extract_evidence(
            "The brake pedal feels soft.",
            max_attempts=2,
        )

    assert result is None