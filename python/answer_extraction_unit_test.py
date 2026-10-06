from unittest.mock import patch
import urllib.error

from diagnostic_schema import FrequencyAnswer
from answer_extraction_test import (
    extract_answer,
    extract_starting_behaviour,
)

def test_extract_answer_timeout():

    with patch(
        "answer_extraction_test.urllib.request.urlopen"
    ) as mock_urlopen:

        mock_urlopen.side_effect = (
            TimeoutError("Request timed out")
        )

        result = extract_answer(
            "It happens once a week.",
            "frequency",
        )

    assert result is None


def test_extract_starting_behaviour():

    fake_response = (
        '{"starting_behaviour": '
        '"turns over slowly"}'
    )

    with patch(
        "answer_extraction_test.urllib.request.urlopen"
    ) as mock_urlopen:

        mock_response = mock_urlopen.return_value

        mock_response.read.return_value = (
            '{"response": '
            '"{\\"starting_behaviour\\": '
            '\\"turns over slowly\\"}"}'
        ).encode()

        result = extract_starting_behaviour(
            "It turns over slowly."
        )

    assert result.starting_behaviour == (
        "turns over slowly"
    )


def test_extract_answer():

    with patch(
        "answer_extraction_test.urllib.request.urlopen"
    ) as mock_urlopen:

        mock_response = mock_urlopen.return_value

        mock_response.read.return_value = (
            '{"response": '
            '"{\\"information_type\\": '
            '\\"warning_lights\\", '
            '\\"answer\\": '
            '\\"The engine warning light is on.\\"}"}'
        ).encode()

        result = extract_answer(
            "The engine warning light is on.",
            "warning_lights",
        )

    assert result.information_type == (
        "warning_lights"
    )

    assert result.answer == (
        "The engine warning light is on."
    )

def test_extract_answer_returns_unknown():

    with patch(
        "answer_extraction_test.urllib.request.urlopen"
    ) as mock_urlopen:

        mock_response = mock_urlopen.return_value

        mock_response.read.return_value = (
            '{"response": '
            '"{\\"information_type\\": '
            '\\"warning_lights\\", '
            '\\"answer\\": \\"unknown\\"}"}'
        ).encode()

        result = extract_answer(
            "I'm not sure.",
            "warning_lights",
        )

    assert result.information_type == (
        "warning_lights"
    )

    assert result.answer == "unknown"

def test_extract_answer_frequency():

    with patch(
        "answer_extraction_test.urllib.request.urlopen"
    ) as mock_urlopen:

        mock_response = mock_urlopen.return_value

        mock_response.read.return_value = (
            '{"response": '
            '"{\\"information_type\\": '
            '\\"frequency\\", '
            '\\"answer\\": '
            '\\"It happens once or twice a week.\\"}"}'
        ).encode()

        result = extract_answer(
            "It happens once or twice a week.",
            "frequency",
        )

    assert result.information_type == (
        "frequency"
    )

    assert result.answer == (
        "It happens once or twice a week."
    )

def test_extract_answer_starting_behaviour():

    with patch(
        "answer_extraction_test.urllib.request.urlopen"
    ) as mock_urlopen:

        mock_response = mock_urlopen.return_value

        mock_response.read.return_value = (
            '{"response": '
            '"{\\"information_type\\": '
            '\\"starting_behaviour\\", '
            '\\"answer\\": '
            '\\"It turns over slowly.\\"}"}'
        ).encode()

        result = extract_answer(
            "It turns over slowly.",
            "starting_behaviour",
        )

    assert result.information_type == (
        "starting_behaviour"
    )

    assert result.answer == (
        "It turns over slowly."
    )

def test_extract_answer_invalid_json():

    with patch(
        "answer_extraction_test.urllib.request.urlopen"
    ) as mock_urlopen:

        mock_response = mock_urlopen.return_value

        mock_response.read.return_value = (
            '{"response": '
            '"This is not valid JSON"}'
        ).encode()

        result = extract_answer(
            "It happens once a week.",
            "frequency",
        )

    assert result is None

def test_extract_answer_invalid_structure():

    with patch(
        "answer_extraction_test.urllib.request.urlopen"
    ) as mock_urlopen:

        mock_response = mock_urlopen.return_value

        mock_response.read.return_value = (
            '{"response": '
            '"{\\"information_type\\": '
            '\\"frequency\\"}"}'
        ).encode()

        result = extract_answer(
            "It happens once a week.",
            "frequency",
        )

    assert result is None

def test_extract_answer_request_failure():

    with patch(
        "answer_extraction_test.urllib.request.urlopen"
    ) as mock_urlopen:

        mock_urlopen.side_effect = (
            urllib.error.URLError("Connection failed")
        )

        result = extract_answer(
            "It happens once a week.",
            "frequency",
        )

    assert result is None

def test_frequency_answer_schema():

    answer = FrequencyAnswer(
        frequency="once or twice a week"
    )

    assert answer.frequency == (
        "once or twice a week"
    )