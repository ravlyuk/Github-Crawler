# tests/test_proxy.py
import pytest

from src.proxy import format_proxy, proxy_filter


@pytest.mark.asyncio
async def test_format_proxy_adds_http_scheme() -> None:
    proxies = ["127.0.0.1:8080", "example.com:3128"]
    result = await format_proxy(proxies)
    assert result == ["http://127.0.0.1:8080", "http://example.com:3128"]


@pytest.mark.asyncio
async def test_format_proxy_preserves_existing_http() -> None:
    proxies = ["http://1.2.3.4:80", "http://proxy.local:8080"]
    result = await format_proxy(proxies)
    assert result == proxies


@pytest.mark.asyncio
async def test_format_proxy_empty_list() -> None:

    result = await format_proxy([])
    assert result == []

