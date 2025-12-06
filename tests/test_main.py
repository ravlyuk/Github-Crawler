import json
from unittest.mock import mock_open, patch

import pytest

from src.main import read_input_json, validate_data, save_output_json, parse_args
from src.schemas import SearchParams


def test_read_input_json():
    """Test reading valid JSON file."""
    mock_data = {
        "keywords": ["test"],
        "type": "Repositories",
        "proxies": ["127.0.0.1:8080"],
    }

    with patch(target="builtins.open", new=mock_open(read_data=json.dumps(mock_data))):
        result = read_input_json("test.json")
        assert result == mock_data


def test_validate_data_valid():
    """Test validating correct data."""
    data = {
        "keywords": ["fastapi", "pydantic"],
        "type": "Repositories",
        "proxies": ["127.0.0.1:8080"],
    }

    result = validate_data(data)
    assert isinstance(result, SearchParams)


def test_validate_data_invalid():
    """Test validating invalid data exits."""

    data = {"keywords": ["test"], "type": "InvalidType", "proxies": ["127.0.0.1:8080"]}

    with pytest.raises(SystemExit):
        validate_data(data)


def test_save_output_json():
    """Test saving data to JSON."""
    data = [{"url": "https://github.com/test/repo"}]

    mock_file = mock_open()
    with patch("builtins.open", mock_file):
        save_output_json("output.json", data)
        mock_file.assert_called_once_with("output.json", "w", encoding="utf-8")


def test_parse_args_with_valid_arguments():
    """Test parse_args with valid input and output arguments."""
    test_args = ["prog", "-i", "input.json", "-o", "output.json"]

    with patch("sys.argv", test_args):
        args = parse_args()
        assert args.input == "input.json"
        assert args.output == "output.json"
