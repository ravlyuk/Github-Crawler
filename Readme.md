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

## Usage

### Running the Application

1. Configure your search parameters in `src/input.json`:
```json
{
  "keywords": ["openstack", "nova", "css"],
  "proxies": ["194.126.37.94:8080", "13.78.125.167:8080"],
  "type": "Repositories"
}
```

2. Run the crawler:
```bash
poetry run python -m src.main
```

3. Results will be saved to `src/output.json`

### Available Search Types

- `Repositories` - Search for GitHub repositories (includes extra metadata)
- `Wikis` - Search for GitHub wiki pages
- `Issues` - Search for GitHub issues pages

## Testing

### Run All Tests

```bash
poetry run pytest -v
```
### Show Coverage Percentage Only

```bash
poetry run pytest --cov=src
```
