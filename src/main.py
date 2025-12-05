import asyncio
import json

from loguru import logger
from pydantic import ValidationError

from src.schemas import SearchParams
from src.crawler import get_search_results


def read_input_json(file_name: str) -> dict:
    logger.info(f"Reading input file {file_name}")
    with open(file_name, "r") as input_json:
        return json.load(input_json)


def validate_data(args: dict) -> SearchParams | None:
    logger.info(f"Validating input data")
    try:
        return SearchParams(**args)
    except ValidationError as e:
        logger.error(e.errors()[0]["msg"])
        exit(1)


def save_output_json(file_name: str, data: list) -> None:
    logger.info(f"Saving output file {file_name}")
    with open(file_name, "w") as f:
        return json.dump(data, f, indent=4)


def main():
    # read input data
    request = read_input_json(file_name="src/input.json")

    # validate data
    search_params = validate_data(request)

    # parse data
    result = asyncio.run(get_search_results(search_params))

    # save output data
    save_output_json(file_name="src/output.json", data=result)

    logger.info("Finished!")


# openstack nova css
if __name__ == "__main__":
    main()
