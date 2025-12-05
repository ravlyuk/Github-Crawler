import asyncio
import time

import httpx
from loguru import logger

from src.config import CHECK_URL, TIMEOUT_FILTER_SECOND


async def format_proxy(proxies: list[str]) -> list[str]:
    return [
        proxy if proxy.startswith("http://") else f"http://{proxy}" for proxy in proxies
    ]


async def check_proxy(proxy: str) -> tuple[str, float] | None:
    start_time = time.time()

    try:

        async with httpx.AsyncClient(proxy=proxy) as proxy_client:
            response = await proxy_client.get(
                CHECK_URL,
                timeout=TIMEOUT_FILTER_SECOND,
            )

            if response.status_code == 200:
                latency = time.time() - start_time
                logger.info(
                    f"Proxy {proxy} is working with latency {latency:.2f} seconds"
                )
                return proxy, latency
            else:
                logger.error(f"Proxy {proxy} is not working")

    except Exception as e:
        logger.error(f"Proxy {proxy} is not working")


async def proxy_filter(proxies: list[str]) -> list[str]:

    tasks = [check_proxy(proxy) for proxy in proxies]
    results = await asyncio.gather(*tasks)
    live_proxies = [result for result in results if result is not None]
    live_proxies.sort(key=lambda x: x[1])  # sort by latency
    live_proxies = [proxy[0] for proxy in live_proxies]  # extract proxy strings
    logger.info(f"Proxies checked: {len(results)}, working found: {len(live_proxies)} ")
    return live_proxies
