import pathlib
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.crawler import get_search_results, get_repository_extra_data
from src.schemas import SearchParams, TypeEnum


# --- Fixtures -----------------------------------------------------------------


@pytest.fixture
def mock_wiki_search_html() -> str:
    """Return HTML content from `MockWikiSearch.html` in this test folder."""

    html_path = pathlib.Path(__file__).parent / "mock_html/MockWikiSearch.html"
    return html_path.read_text(encoding="utf-8")


@pytest.fixture
def mock_repository_search_html() -> str:
    """Return HTML content from `MockWikiSearch.html` in this test folder."""

    html_path = pathlib.Path(__file__).parent / "mock_html/MockRepositorySearch.html"
    return html_path.read_text(encoding="utf-8")


@pytest.fixture
def wiki_search_params() -> SearchParams:
    """Common search params for wiki search used in tests."""

    return SearchParams(
        keywords=["openstack", "nova", "css"],
        type=TypeEnum.WIKIS,
        proxies=["127.0.0.1:8080"],
    )


@pytest.fixture
def repository_search_params() -> SearchParams:
    """Common search params for wiki search used in tests."""

    return SearchParams(
        keywords=["openstack", "nova", "css"],
        type=TypeEnum.REPOSITORIES,
        proxies=["127.0.0.1:8080"],
    )


@pytest.fixture
def repo_search_params() -> SearchParams:
    """Search params for repositories used in the "no proxies" test."""

    return SearchParams(
        keywords=["python"],
        type=TypeEnum.REPOSITORIES,
        proxies=["127.0.0.1:8080"],
    )


# --- Tests --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_wiki_results_success(
    mock_wiki_search_html: str, wiki_search_params: SearchParams
) -> None:
    """get_search_results returns URLs parsed from the mocked search HTML."""

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.get.return_value = MagicMock(
        status_code=200,
        text=mock_wiki_search_html,
    )

    with patch("src.crawler.httpx.AsyncClient", return_value=mock_client):
        result = await get_search_results(wiki_search_params)

    expected = [
        {
            "url": "https://github.com/vault-team/vault-website/wiki/Quick-installation-guide"
        },
        {
            "url": "https://github.com/marcosaletta/Juno-CentOS7-Guide/wiki/2.-Controller-and-Network-Node-Installation"
        },
        {"url": "https://github.com/escrevebastante/tongue/wiki/Home"},
        {"url": "https://github.com/dellcloudedge/crowbar/wiki/Release-notes"},
        {"url": "https://github.com/eryeru12/crowbar/wiki/Release-notes"},
        {"url": "https://github.com/MirantisDellCrowbar/crowbar/wiki/Release-notes"},
        {"url": "https://github.com/vinayakponangi/crowbar/wiki/Release-notes"},
        {"url": "https://github.com/opencit/opencit/wiki/Open-CIT-3.2-Product-Guide"},
        {"url": "https://github.com/opencit/opencit/wiki/Open-CIT-3.2.1-Product-Guide"},
        {"url": "https://github.com/westurner/tools/wiki/index"},
    ]

    assert result == expected
    assert all("extra" not in item for item in result)


@pytest.mark.asyncio
async def test_get_repository_results_success(
    mock_repository_search_html: str, repository_search_params: SearchParams
) -> None:

    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.get.return_value = MagicMock(
        status_code=200,
        text=mock_repository_search_html,
    )

    with patch("src.crawler.httpx.AsyncClient", return_value=mock_client):
        result = await get_search_results(repository_search_params)

    expected = [
        {
            "url": "https://github.com/atuldjadhav/DropBox-Cloud-Storage",
            "extra": {
                "owner": None,
                "language_stats": {"CSS": None, "JavaScript": None, "HTML": None},
            },
        },
        {
            "url": "https://github.com/michealbalogun/Horizon-dashboard",
            "extra": {
                "owner": None,
                "language_stats": {"CSS": None, "JavaScript": None, "HTML": None},
            },
        },
    ]

    assert result == expected


@pytest.mark.asyncio
async def test_get_search_results_no_proxies(repo_search_params: SearchParams) -> None:
    """If proxy_filter returns empty list, get_search_results returns empty list."""

    with (
        patch("src.crawler.format_proxy", new_callable=AsyncMock) as mock_format,
        patch("src.crawler.proxy_filter", new_callable=AsyncMock) as mock_filter,
    ):
        mock_format.return_value = ["http://127.0.0.1:8080"]
        mock_filter.return_value = []  # Simulate no working proxies

        result = await get_search_results(repo_search_params)

    assert result == []
    mock_format.assert_awaited_once_with(repo_search_params.proxies)
    mock_filter.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_repository_extra_data_http_status_error() -> None:
    """When response raises HTTPStatusError, return extra as None."""

    mock_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "404 Not Found", request=MagicMock(), response=MagicMock()
    )
    mock_client.get.return_value = mock_response

    result = await get_repository_extra_data(
        mock_client, "https://github.com/test/repo"
    )

    assert result == {"url": "https://github.com/test/repo", "extra": None}

