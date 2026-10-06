from unittest.mock import patch

from question_generation_test import DiagnosticQuestion, generate_question


def test_generate_question_returns_valid_question():
    fake_response = {
        "response": (
            '{"question": '
            '"When starting the engine, does it turn over normally, '
            'slowly, or not at all?"}'
        )
    }

    with patch(
        "question_generation_test.urllib.request.urlopen"
    ) as mock_urlopen:
        mock_response = mock_urlopen.return_value
        mock_response.read.return_value = (
            '{"response": "{\\"question\\": '
            '\\"When starting the engine, does it turn over normally, '
            'slowly, or not at all?\\"}"}'
        ).encode()

        result = generate_question("starting_behaviour")

    assert isinstance(result, DiagnosticQuestion)
    assert result.question
    assert "normally" in result.question.lower()
    assert "slowly" in result.question.lower()
    assert "not at all" in result.question.lower()