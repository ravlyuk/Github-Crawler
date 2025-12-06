# GitHub Crawler

A Python-based asynchronous web crawler for searching GitHub repositories and wikis with proxy support.
## Project Structure

```
Github-Crawler/
├── src/
│   ├── config.py       # Configuration and XPath selectors
│   ├── crawler.py      # Main crawling logic
│   ├── proxy.py        # Proxy validation and formatting
│   ├── schemas.py      # Pydantic models
│   ├── main.py         # Entry point
│   ├── input.json      # Search parameters
│   └── output.json     # Crawl results
└── tests/
    ├── test_crawler.py # Crawler tests
    ├── test_proxy.py   # Proxy tests
    ├── test_main.py    # Integration tests
    └── mock_html/      # Mock HTML files for testing
```

## Requirements

- Python 3.13+
- Poetry for dependency management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ravlyuk/Github-Crawler.git
```
```bash
cd Github-Crawler
```


2. Install dependencies using Poetry:
```bash
poetry install --no-root
```

**Note:** You don't need to manually activate the virtual environment. Poetry automatically manages it when you use `poetry run` commands.


## Usage

### Running the Application

1. Configure your search parameters in an input JSON file (e.g., `input.json`):
```json
{
  "keywords": ["openstack", "nova", "css"],
  "proxies": ["194.126.37.94:8080", "13.78.125.167:8080"],
  "type": "Repositories"
}
```

2. Run the crawler from the command line:
```bash
poetry run python -m src.main -i input.json -o output.json
```
The application accepts command-line arguments to specify input and output files:
- `-i` or `--input` — path to the input JSON file (required)
- `-o` or `--output` — path to the output JSON file (required)
- `-h` or `--help` — show help message with examples

3. Results will be saved to the specified output file.

### Get Help

To see all available options and examples:
```bash
poetry run python -m src.main --help
```

### Available Search Types

- `Repositories` - Search for GitHub repositories (includes extra metadata)
- `Issues` - Search for GitHub issues
- `Wikis` - Search for GitHub wiki pages

## Testing

### Run All Tests with Verbose Output

```bash
poetry run pytest -v
```

### Run Tests with Coverage Report

```bash
poetry run pytest --cov=src
```

This will show you the percentage of code covered by tests for each module.
