from __future__ import annotations

import os
from typing import Any

import httpx

from ._constants import API_KEY_ENV_VAR, DEFAULT_BASE_URL, DEFAULT_TIMEOUT
from ._exceptions import (
    APIConnectionError,
    APITimeoutError,
    _make_api_error,
)
from ._version import __version__
from .resources.mandates import AsyncMandates, Mandates
from .resources.matches import AsyncMatches, Matches


class OpenMandate:
    """Synchronous client for the OpenMandate API.

    Usage::

        from openmandate import OpenMandate

        client = OpenMandate(api_key="om_live_...")
        mandate = client.mandates.create(category="cofounder")

    If ``api_key`` is not provided, the client reads from the
    ``OPENMANDATE_API_KEY`` environment variable.
    """

    mandates: Mandates
    matches: Matches

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.api_key = api_key or os.environ.get(API_KEY_ENV_VAR, "")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Pass api_key= or set the "
                f"{API_KEY_ENV_VAR} environment variable."
            )

        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout if timeout is not None else DEFAULT_TIMEOUT

        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self._default_headers(),
        )

        self.mandates = Mandates(self._client, self._request)
        self.matches = Matches(self._client, self._request)

    def _default_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"openmandate-python/{__version__}",
        }

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Make an HTTP request and return the parsed JSON body.

        Raises the appropriate exception for error responses.
        """
        try:
            response = self._client.request(
                method,
                path,
                params=params,
                json=json,
            )
        except httpx.TimeoutException as exc:
            raise APITimeoutError(
                f"Request timed out: {method} {path}"
            ) from exc
        except httpx.ConnectError as exc:
            raise APIConnectionError(
                f"Failed to connect: {method} {path}"
            ) from exc

        if response.status_code >= 400:
            try:
                body = response.json()
            except ValueError:
                body = None
            raise _make_api_error(response.status_code, body)

        if response.status_code == 204:
            return None

        return response.json()

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> OpenMandate:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"OpenMandate(base_url={self.base_url!r})"


class AsyncOpenMandate:
    """Asynchronous client for the OpenMandate API.

    Usage::

        import asyncio
        from openmandate import AsyncOpenMandate

        async def main():
            client = AsyncOpenMandate(api_key="om_live_...")
            mandate = await client.mandates.create(category="cofounder")
            await client.close()

        asyncio.run(main())

    If ``api_key`` is not provided, the client reads from the
    ``OPENMANDATE_API_KEY`` environment variable.
    """

    mandates: AsyncMandates
    matches: AsyncMatches

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.api_key = api_key or os.environ.get(API_KEY_ENV_VAR, "")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Pass api_key= or set the "
                f"{API_KEY_ENV_VAR} environment variable."
            )

        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout if timeout is not None else DEFAULT_TIMEOUT

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self._default_headers(),
        )

        self.mandates = AsyncMandates(self._client, self._request)
        self.matches = AsyncMatches(self._client, self._request)

    def _default_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"openmandate-python/{__version__}",
        }

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Make an async HTTP request and return the parsed JSON body.

        Raises the appropriate exception for error responses.
        """
        try:
            response = await self._client.request(
                method,
                path,
                params=params,
                json=json,
            )
        except httpx.TimeoutException as exc:
            raise APITimeoutError(
                f"Request timed out: {method} {path}"
            ) from exc
        except httpx.ConnectError as exc:
            raise APIConnectionError(
                f"Failed to connect: {method} {path}"
            ) from exc

        if response.status_code >= 400:
            try:
                body = response.json()
            except ValueError:
                body = None
            raise _make_api_error(response.status_code, body)

        if response.status_code == 204:
            return None

        return response.json()

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncOpenMandate:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    def __repr__(self) -> str:
        return f"AsyncOpenMandate(base_url={self.base_url!r})"
