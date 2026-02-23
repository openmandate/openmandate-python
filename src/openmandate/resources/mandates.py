from __future__ import annotations

import time
from typing import Any, Callable

import httpx

from .._exceptions import APITimeoutError
from .._pagination import AsyncPage, SyncPage
from ..types.mandate import Mandate
from ..types.params import AnswerParam, ContactParam, CorrectionParam


class Mandates:
    """Sync resource for managing mandates."""

    def __init__(self, client: httpx.Client, request: Callable[..., Any]) -> None:
        self._client = client
        self._request = request

    def create(
        self,
        *,
        category: str = "",
        contact: ContactParam | None = None,
    ) -> Mandate:
        """Create a new mandate.

        Args:
            category: Freeform category hint (e.g. "cofounder", "recruiting",
                "climate-tech"). Any string accepted. Defaults to empty string.
            contact: Optional contact information.

        Returns:
            The created mandate with initial pending_questions.
        """
        body: dict[str, Any] = {}
        if category:
            body["category"] = category
        if contact is not None:
            body["contact"] = dict(contact)
        data = self._request("POST", "/v1/mandates", json=body)
        return Mandate.model_validate(data)

    def retrieve(self, mandate_id: str) -> Mandate:
        """Get a mandate by ID.

        Args:
            mandate_id: The mandate ID (e.g. "mnd_xxx").

        Returns:
            The mandate.
        """
        data = self._request("GET", f"/v1/mandates/{mandate_id}")
        return Mandate.model_validate(data)

    def list(
        self,
        *,
        status: str | None = None,
        limit: int | None = None,
        next_token: str | None = None,
    ) -> SyncPage[Mandate]:
        """List mandates with optional filtering.

        Args:
            status: Filter by status (e.g. "active", "intake").
            limit: Maximum number of items per page.
            next_token: Pagination cursor from a previous response.

        Returns:
            A page of mandates. Supports auto-pagination via iteration.
        """
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit
        if next_token is not None:
            params["next_token"] = next_token

        data = self._request("GET", "/v1/mandates", params=params)

        def fetch_next(token: str) -> SyncPage[Mandate]:
            return self.list(status=status, limit=limit, next_token=token)

        return SyncPage(
            items=[Mandate.model_validate(item) for item in data["items"]],
            next_token=data.get("next_token"),
            fetch_next=fetch_next,
        )

    def submit_answers(
        self,
        mandate_id: str,
        *,
        answers: list[AnswerParam],
        corrections: list[CorrectionParam] | None = None,
    ) -> Mandate:
        """Submit answers to pending intake questions.

        Args:
            mandate_id: The mandate ID.
            answers: List of answers to submit.
            corrections: Optional list of corrections to previous answers.

        Returns:
            The updated mandate (may have new pending_questions).
        """
        body: dict[str, Any] = {"answers": [dict(a) for a in answers]}
        if corrections is not None:
            body["corrections"] = [dict(c) for c in corrections]
        data = self._request(
            "POST", f"/v1/mandates/{mandate_id}/answers", json=body
        )
        return Mandate.model_validate(data)

    def close(self, mandate_id: str) -> Mandate:
        """Close a mandate.

        Args:
            mandate_id: The mandate ID.

        Returns:
            The closed mandate.
        """
        data = self._request("POST", f"/v1/mandates/{mandate_id}/close")
        return Mandate.model_validate(data)

    def complete_intake(
        self,
        mandate_id: str,
        answer_fn: Callable[[list[Any]], list[AnswerParam]],
    ) -> Mandate:
        """Loop through the intake flow until all questions are answered.

        Repeatedly fetches the mandate, calls ``answer_fn`` with the pending
        questions, submits the answers, and repeats until there are no more
        pending questions.

        Args:
            mandate_id: The mandate ID.
            answer_fn: A callable that receives a list of
                :class:`~openmandate.types.shared.Question` objects and returns
                a list of :class:`~openmandate.types.params.AnswerParam` dicts.

        Returns:
            The mandate after intake is complete.
        """
        mandate = self.retrieve(mandate_id)
        while mandate.pending_questions:
            answers = answer_fn(mandate.pending_questions)
            mandate = self.submit_answers(mandate_id, answers=answers)
        return mandate

    def wait_for_match(
        self,
        mandate_id: str,
        *,
        timeout: float = 300.0,
        poll_interval: float = 5.0,
    ) -> Mandate:
        """Poll a mandate until its status becomes ``matched``.

        Args:
            mandate_id: The mandate ID.
            timeout: Maximum seconds to wait. Defaults to 300 (5 minutes).
            poll_interval: Seconds between polls. Defaults to 5.

        Returns:
            The mandate with status ``matched``.

        Raises:
            APITimeoutError: If the timeout elapses without a match.
        """
        deadline = time.monotonic() + timeout
        while True:
            mandate = self.retrieve(mandate_id)
            if mandate.status == "matched":
                return mandate
            if time.monotonic() >= deadline:
                raise APITimeoutError(
                    f"Mandate {mandate_id} did not match within {timeout}s. "
                    f"Current status: {mandate.status}"
                )
            remaining = deadline - time.monotonic()
            time.sleep(min(poll_interval, max(remaining, 0)))


class AsyncMandates:
    """Async resource for managing mandates."""

    def __init__(self, client: httpx.AsyncClient, request: Callable[..., Any]) -> None:
        self._client = client
        self._request = request

    async def create(
        self,
        *,
        category: str = "",
        contact: ContactParam | None = None,
    ) -> Mandate:
        """Create a new mandate.

        Args:
            category: Freeform category hint (e.g. "cofounder", "recruiting",
                "climate-tech"). Any string accepted. Defaults to empty string.
            contact: Optional contact information.

        Returns:
            The created mandate with initial pending_questions.
        """
        body: dict[str, Any] = {}
        if category:
            body["category"] = category
        if contact is not None:
            body["contact"] = dict(contact)
        data = await self._request("POST", "/v1/mandates", json=body)
        return Mandate.model_validate(data)

    async def retrieve(self, mandate_id: str) -> Mandate:
        """Get a mandate by ID.

        Args:
            mandate_id: The mandate ID (e.g. "mnd_xxx").

        Returns:
            The mandate.
        """
        data = await self._request("GET", f"/v1/mandates/{mandate_id}")
        return Mandate.model_validate(data)

    async def list(
        self,
        *,
        status: str | None = None,
        limit: int | None = None,
        next_token: str | None = None,
    ) -> AsyncPage[Mandate]:
        """List mandates with optional filtering.

        Args:
            status: Filter by status (e.g. "active", "intake").
            limit: Maximum number of items per page.
            next_token: Pagination cursor from a previous response.

        Returns:
            An async page of mandates. Supports auto-pagination via async iteration.
        """
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit
        if next_token is not None:
            params["next_token"] = next_token

        data = await self._request("GET", "/v1/mandates", params=params)

        async def fetch_next(token: str) -> AsyncPage[Mandate]:
            return await self.list(status=status, limit=limit, next_token=token)

        return AsyncPage(
            items=[Mandate.model_validate(item) for item in data["items"]],
            next_token=data.get("next_token"),
            fetch_next=fetch_next,
        )

    async def submit_answers(
        self,
        mandate_id: str,
        *,
        answers: list[AnswerParam],
        corrections: list[CorrectionParam] | None = None,
    ) -> Mandate:
        """Submit answers to pending intake questions.

        Args:
            mandate_id: The mandate ID.
            answers: List of answers to submit.
            corrections: Optional list of corrections to previous answers.

        Returns:
            The updated mandate (may have new pending_questions).
        """
        body: dict[str, Any] = {"answers": [dict(a) for a in answers]}
        if corrections is not None:
            body["corrections"] = [dict(c) for c in corrections]
        data = await self._request(
            "POST", f"/v1/mandates/{mandate_id}/answers", json=body
        )
        return Mandate.model_validate(data)

    async def close(self, mandate_id: str) -> Mandate:
        """Close a mandate.

        Args:
            mandate_id: The mandate ID.

        Returns:
            The closed mandate.
        """
        data = await self._request("POST", f"/v1/mandates/{mandate_id}/close")
        return Mandate.model_validate(data)

    async def complete_intake(
        self,
        mandate_id: str,
        answer_fn: Callable[[list[Any]], list[AnswerParam]],
    ) -> Mandate:
        """Loop through the intake flow until all questions are answered.

        Repeatedly fetches the mandate, calls ``answer_fn`` with the pending
        questions, submits the answers, and repeats until there are no more
        pending questions.

        Args:
            mandate_id: The mandate ID.
            answer_fn: A callable that receives a list of
                :class:`~openmandate.types.shared.Question` objects and returns
                a list of :class:`~openmandate.types.params.AnswerParam` dicts.
                May be sync or async.

        Returns:
            The mandate after intake is complete.
        """
        import asyncio
        import inspect

        mandate = await self.retrieve(mandate_id)
        while mandate.pending_questions:
            result = answer_fn(mandate.pending_questions)
            if inspect.isawaitable(result):
                answers = await result
            else:
                answers = result
            mandate = await self.submit_answers(mandate_id, answers=answers)
        return mandate

    async def wait_for_match(
        self,
        mandate_id: str,
        *,
        timeout: float = 300.0,
        poll_interval: float = 5.0,
    ) -> Mandate:
        """Poll a mandate until its status becomes ``matched``.

        Args:
            mandate_id: The mandate ID.
            timeout: Maximum seconds to wait. Defaults to 300 (5 minutes).
            poll_interval: Seconds between polls. Defaults to 5.

        Returns:
            The mandate with status ``matched``.

        Raises:
            APITimeoutError: If the timeout elapses without a match.
        """
        import asyncio

        deadline = time.monotonic() + timeout
        while True:
            mandate = await self.retrieve(mandate_id)
            if mandate.status == "matched":
                return mandate
            if time.monotonic() >= deadline:
                raise APITimeoutError(
                    f"Mandate {mandate_id} did not match within {timeout}s. "
                    f"Current status: {mandate.status}"
                )
            remaining = deadline - time.monotonic()
            await asyncio.sleep(min(poll_interval, max(remaining, 0)))
