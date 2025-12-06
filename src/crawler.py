import asyncio

import httpx
from loguru import logger
from lxml import html

from src.config import Connection, Path
from src.proxy import proxy_filter, format_proxy
from src.schemas import SearchParams, TypeEnum


async def get_search_results(search_params: SearchParams) -> list[dict]:
    """Get search results from main page"""
    result = []
    logger.debug("Start proxy checking...")
    proxies = await format_proxy(search_params.proxies)
    best_proxies = await proxy_filter(proxies)

    if not best_proxies:
        logger.warning("No working proxies available")
        return result

    for proxy in best_proxies:
        logger.debug(f"Using proxy {proxy}")
        try:
            async with httpx.AsyncClient(
                proxy=proxy,
                timeout=Connection.TIMEOUT_SECOND,
                limits=httpx.Limits(max_connections=Connection.MAX_CONNECTIONS),
            ) as client:
                response = await client.get(
                    url=Connection.SEARCH_URL,
                    params={
                        "q": " ".join(search_params.keywords),
                        "type": search_params.type.value,
                    },
                )

                tree = html.fromstring(response.text)
                tree.make_links_absolute(Connection.BASE_URL)
                urls = tree.xpath(Path.ITEM_LINK_XPATH)

                if response.status_code == 200:
                    logger.info(
                        f"Request success with proxy {proxy} to url {response.url}"
                    )
                    if search_params.type == TypeEnum.REPOSITORIES:
                        tasks = [get_repository_extra_data(client, url) for url in urls]
                        result = await asyncio.gather(*tasks)
                    else:
                        result = [{"url": url} for url in urls]

                    break

        except httpx.RequestError:
            logger.error(f"Request failed with proxy {proxy}")

    return result


async def get_repository_extra_data(client: httpx.AsyncClient, url: str) -> dict:
    """Get extra data from repository page."""
    logger.info(f"Getting extra data from repository {url}")
    try:
        response = await client.get(url)
        response.raise_for_status()
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        logger.warning(f"Failed to get extra data {url}: {exc}")
        return {"url": url, "extra": None}

    tree = html.fromstring(response.text)

    owner, css, html_, js = (
        tree.xpath(Path.USERNAME_VALUE_XPATH),
        tree.xpath(Path.CSS_VALUE_XPATH),
        tree.xpath(Path.HTML_VALUE_XPATH),
        tree.xpath(Path.JS_VALUE_XPATH),
    )

    extra_data = {
        "url": url,
        "extra": {
            "owner": owner[0] if owner else None,
            "language_stats": {
                "CSS": css[0] if css else None,
                "JavaScript": js[0] if js else None,
                "HTML": html_[0] if html_ else None,
            },
        },
    }

    return extra_data
