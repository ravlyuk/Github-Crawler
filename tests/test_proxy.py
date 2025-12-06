import pytest

from src.proxy import format_proxy


@pytest.mark.asyncio
async def test_format_proxy_adds_http_scheme() -> None:
    """Test that format_proxy adds 'http://' to proxies without scheme."""
    proxies = ["127.0.0.1:8080", "example.com:3128"]
    result = await format_proxy(proxies)
    assert result == ["http://127.0.0.1:8080", "http://example.com:3128"]


@pytest.mark.asyncio
async def test_format_proxy_preserves_existing_http() -> None:
    """Test that format_proxy preserves proxies with existing 'http://' scheme."""
    proxies = ["http://1.2.3.4:80", "http://proxy.local:8080"]
    result = await format_proxy(proxies)
    assert result == proxies


@pytest.mark.asyncio
async def test_format_proxy_empty_list() -> None:
    """Test that format_proxy handles empty list."""
    result = await format_proxy([])
    assert result == []
