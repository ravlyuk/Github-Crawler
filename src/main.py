import asyncio
import json
import sys
import argparse

from loguru import logger
from pydantic import ValidationError

from src.schemas import SearchParams
from src.crawler import get_search_results


def read_input_json(file_name: str) -> dict:
    """Read input JSON file and return as dictionary."""
    logger.info(f"Reading input file {file_name}")
    with open(file_name, "r", encoding="utf-8") as input_json:
        return json.load(input_json)


def validate_data(data: dict) -> SearchParams | None:
    """Validate input data against SearchParams schema."""
    logger.info("Validating input data")
    try:
        return SearchParams(**data)
    except ValidationError as e:
        logger.error(e.errors()[0]["msg"])
        sys.exit(1)


def save_output_json(file_name: str, data: list) -> None:
    """Save output data to JSON file."""
    logger.info(f"Saving output file {file_name}")
    with open(file_name, "w", encoding="utf-8") as f:
        return json.dump(data, f, indent=4)


help_text = """
EXAMPLES:
  python -m src.main -i input.json -o output.json

RUNNING TESTS:
  poetry run pytest -v                     
  poetry run pytest --cov=src 

INPUT FILE FORMAT:
  {
    "keywords": ["keyword1", "keyword2"],
    "type": "Repositories",
    "proxies": ["proxy1:port", "proxy2:port"]
  }

AVAILABLE SEARCH TYPES:
  - Repositories
  - Issues
  - Wikis
"""


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="GitHub Search Crawler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=help_text,
    )
    parser.add_argument("-i", "--input", required=True, help="Input JSON file path")
    parser.add_argument("-o", "--output", required=True, help="Output JSON file path")
    return parser.parse_args()


def main(input_file: str, output_file: str) -> None:
    """Main function to run the crawler."""
    logger.info("Starting...")

    request = read_input_json(input_file)
    search_params = validate_data(request)
    result = asyncio.run(get_search_results(search_params))
    save_output_json(output_file, result)

    logger.info("Finished!")


if __name__ == "__main__":
    args = parse_args()
    main(input_file=args.input, output_file=args.output)
