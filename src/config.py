from pydantic_settings import BaseSettings


class Connection:
    """Connection settings."""

    BASE_URL: str = "https://github.com"
    SEARCH_URL: str = "https://github.com/search"
    CHECK_URL: str = "https://icanhazip.com/"
    TIMEOUT_SECOND: int = 5
    TIMEOUT_FILTER_SECOND: int = 5
    MAX_CONNECTIONS: int = 20


class Path:
    """XPath expressions for parsing HTML."""
    ITEM_LINK_XPATH = '//div[contains(@class, "search-title")]/a/@href'
    CSS_VALUE_XPATH = '//a[contains(@href, "search?l=css")]/span[2]/text()'
    HTML_VALUE_XPATH = '//a[contains(@href, "search?l=html")]/span[2]/text()'
    JS_VALUE_XPATH = '//a[contains(@href, "search?l=javascript")]/span[2]/text()'
    USERNAME_VALUE_XPATH = '//meta[@name="octolytics-dimension-user_login"]/@content'
