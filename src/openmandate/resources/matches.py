from __future__ import annotations

from typing import Any, Callable

import httpx

from .._pagination import AsyncPage, SyncPage
from ..types.match import Match


class Matches:
    """Sync resource for managing matches."""

    def __init__(self, client: httpx.Client, request: Callable[..., Any]) -> None:
        self._client = client
        self._request = request

    def list(
        self,
        *,
        limit: int | None = None,
        next_token: str | None = None,
    ) -> SyncPage[Match]:
        """List matches.

        Args:
            limit: Maximum number of items per page.
            next_token: Pagination cursor from a previous response.

        Returns:
            A page of matches. Supports auto-pagination via iteration.
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if next_token is not None:
            params["next_token"] = next_token

        data = self._request("GET", "/v1/matches", params=params)

        def fetch_next(token: str) -> SyncPage[Match]:
            return self.list(limit=limit, next_token=token)

        return SyncPage(
            items=[Match.model_validate(item) for item in data["items"]],
            next_token=data.get("next_token"),
            fetch_next=fetch_next,
        )

    def retrieve(self, match_id: str) -> Match:
        """Get a match by ID.

        Args:
            match_id: The match ID (e.g. "m_xxx").

        Returns:
            The match.
        """
        data = self._request("GET", f"/v1/matches/{match_id}")
        return Match.model_validate(data)

    def accept(self, match_id: str) -> Match:
        """Accept a match.

        Args:
            match_id: The match ID.

        Returns:
            The updated match.
        """
        data = self._request("POST", f"/v1/matches/{match_id}/accept")
        return Match.model_validate(data)

    def decline(self, match_id: str) -> Match:
        """Decline a match.

        Args:
            match_id: The match ID.

        Returns:
            The updated match.
        """
        data = self._request("POST", f"/v1/matches/{match_id}/decline")
        return Match.model_validate(data)

    def submit_outcome(self, match_id: str, outcome: str) -> Match:
        """Submit an outcome for a match.

        Args:
            match_id: The match ID.
            outcome: The outcome value.

        Returns:
            The updated match.
        """
        data = self._request(
            "POST", f"/v1/matches/{match_id}/outcome", json={"outcome": outcome}
        )
        return Match.model_validate(data)


class AsyncMatches:
    """Async resource for managing matches."""

    def __init__(self, client: httpx.AsyncClient, request: Callable[..., Any]) -> None:
        self._client = client
        self._request = request

    async def list(
        self,
        *,
        limit: int | None = None,
        next_token: str | None = None,
    ) -> AsyncPage[Match]:
        """List matches.

        Args:
            limit: Maximum number of items per page.
            next_token: Pagination cursor from a previous response.

        Returns:
            An async page of matches. Supports auto-pagination via async iteration.
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if next_token is not None:
            params["next_token"] = next_token

        data = await self._request("GET", "/v1/matches", params=params)

        async def fetch_next(token: str) -> AsyncPage[Match]:
            return await self.list(limit=limit, next_token=token)

        return AsyncPage(
            items=[Match.model_validate(item) for item in data["items"]],
            next_token=data.get("next_token"),
            fetch_next=fetch_next,
        )

    async def retrieve(self, match_id: str) -> Match:
        """Get a match by ID.

        Args:
            match_id: The match ID (e.g. "m_xxx").

        Returns:
            The match.
        """
        data = await self._request("GET", f"/v1/matches/{match_id}")
        return Match.model_validate(data)

    async def accept(self, match_id: str) -> Match:
        """Accept a match.

        Args:
            match_id: The match ID.

        Returns:
            The updated match.
        """
        data = await self._request("POST", f"/v1/matches/{match_id}/accept")
        return Match.model_validate(data)

    async def decline(self, match_id: str) -> Match:
        """Decline a match.

        Args:
            match_id: The match ID.

        Returns:
            The updated match.
        """
        data = await self._request("POST", f"/v1/matches/{match_id}/decline")
        return Match.model_validate(data)

    async def submit_outcome(self, match_id: str, outcome: str) -> Match:
        """Submit an outcome for a match.

        Args:
            match_id: The match ID.
            outcome: The outcome value.

        Returns:
            The updated match.
        """
        data = await self._request(
            "POST", f"/v1/matches/{match_id}/outcome", json={"outcome": outcome}
        )
        return Match.model_validate(data)
