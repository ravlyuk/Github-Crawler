# Connection
BASE_URL = "https://github.com"
SEARCH_URL = "https://github.com/search"
CHECK_URL = "https://icanhazip.com/"
TIMEOUT_SECOND = 5
TIMEOUT_FILTER_SECOND = 3
MAX_CONNECTIONS = 20

# XPaths
ITEM_LINK_XPATH = '//div[contains(@class, "search-title")]/a/@href'
CSS_VALUE_XPATH = '//a[contains(@href, "search?l=css")]/span[2]/text()'
HTML_VALUE_XPATH = '//a[contains(@href, "search?l=html")]/span[2]/text()'
JS_VALUE_XPATH = '//a[contains(@href, "search?l=javascript")]/span[2]/text()'
USERNAME_VALUE_XPATH = '//meta[@name="octolytics-dimension-user_login"]/@content'
