from __future__ import annotations

from typing import Any, Callable

import httpx

from .._pagination import AsyncPage, SyncPage
from ..types.shared import VerifiedContact


class Contacts:
    """Sync resource for managing verified contacts."""

    def __init__(self, client: httpx.Client, request: Callable[..., Any]) -> None:
        self._client = client
        self._request = request

    def list(
        self,
        *,
        limit: int | None = None,
        next_token: str | None = None,
    ) -> SyncPage[VerifiedContact]:
        """List verified contacts.

        Args:
            limit: Maximum number of items per page.
            next_token: Pagination cursor from a previous response.

        Returns:
            A page of verified contacts. Supports auto-pagination via iteration.
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if next_token is not None:
            params["next_token"] = next_token

        data = self._request("GET", "/v1/contacts", params=params)

        def fetch_next(token: str) -> SyncPage[VerifiedContact]:
            return self.list(limit=limit, next_token=token)

        return SyncPage(
            items=[VerifiedContact.model_validate(item) for item in data["items"]],
            next_token=data.get("next_token"),
            fetch_next=fetch_next,
        )

    def add(
        self,
        contact_type: str,
        contact_value: str,
        *,
        display_label: str | None = None,
    ) -> VerifiedContact:
        """Add a new contact.

        Args:
            contact_type: Type of contact. Currently only "email" is supported.
            contact_value: The contact value (e.g. email address).
            display_label: Optional human-readable label for the contact.

        Returns:
            The created verified contact (status will be "pending").
        """
        body: dict[str, Any] = {
            "contact_type": contact_type,
            "contact_value": contact_value,
        }
        if display_label is not None:
            body["display_label"] = display_label
        data = self._request("POST", "/v1/contacts", json=body)
        return VerifiedContact.model_validate(data)

    def verify(self, contact_id: str, *, code: str) -> VerifiedContact:
        """Verify a contact with a verification code.

        Args:
            contact_id: The contact ID.
            code: The verification code sent to the contact.

        Returns:
            The verified contact (status will be "verified").
        """
        body: dict[str, Any] = {"code": code}
        data = self._request(
            "POST", f"/v1/contacts/{contact_id}/verify", json=body
        )
        return VerifiedContact.model_validate(data)

    def delete(self, contact_id: str) -> dict[str, Any]:
        """Delete a contact.

        Args:
            contact_id: The contact ID.

        Returns:
            Confirmation of deletion.
        """
        data = self._request("DELETE", f"/v1/contacts/{contact_id}")
        return data

    def update(
        self,
        contact_id: str,
        *,
        display_label: str | None = None,
        is_primary: bool | None = None,
    ) -> VerifiedContact:
        """Update a contact.

        Args:
            contact_id: The contact ID.
            display_label: Optional new display label.
            is_primary: Optional flag to set as primary contact.

        Returns:
            The updated verified contact.
        """
        body: dict[str, Any] = {}
        if display_label is not None:
            body["display_label"] = display_label
        if is_primary is not None:
            body["is_primary"] = is_primary
        data = self._request("PATCH", f"/v1/contacts/{contact_id}", json=body)
        return VerifiedContact.model_validate(data)

    def resend_otp(self, contact_id: str) -> VerifiedContact:
        """Resend the verification code for a pending contact.

        Args:
            contact_id: The contact ID.

        Returns:
            The contact (status remains "pending").
        """
        data = self._request("POST", f"/v1/contacts/{contact_id}/resend")
        return VerifiedContact.model_validate(data)


class AsyncContacts:
    """Async resource for managing verified contacts."""

    def __init__(self, client: httpx.AsyncClient, request: Callable[..., Any]) -> None:
        self._client = client
        self._request = request

    async def list(
        self,
        *,
        limit: int | None = None,
        next_token: str | None = None,
    ) -> AsyncPage[VerifiedContact]:
        """List verified contacts.

        Args:
            limit: Maximum number of items per page.
            next_token: Pagination cursor from a previous response.

        Returns:
            An async page of verified contacts. Supports auto-pagination via
            async iteration.
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if next_token is not None:
            params["next_token"] = next_token

        data = await self._request("GET", "/v1/contacts", params=params)

        async def fetch_next(token: str) -> AsyncPage[VerifiedContact]:
            return await self.list(limit=limit, next_token=token)

        return AsyncPage(
            items=[VerifiedContact.model_validate(item) for item in data["items"]],
            next_token=data.get("next_token"),
            fetch_next=fetch_next,
        )

    async def add(
        self,
        contact_type: str,
        contact_value: str,
        *,
        display_label: str | None = None,
    ) -> VerifiedContact:
        """Add a new contact.

        Args:
            contact_type: Type of contact. Currently only "email" is supported.
            contact_value: The contact value (e.g. email address).
            display_label: Optional human-readable label for the contact.

        Returns:
            The created verified contact (status will be "pending").
        """
        body: dict[str, Any] = {
            "contact_type": contact_type,
            "contact_value": contact_value,
        }
        if display_label is not None:
            body["display_label"] = display_label
        data = await self._request("POST", "/v1/contacts", json=body)
        return VerifiedContact.model_validate(data)

    async def verify(self, contact_id: str, *, code: str) -> VerifiedContact:
        """Verify a contact with a verification code.

        Args:
            contact_id: The contact ID.
            code: The verification code sent to the contact.

        Returns:
            The verified contact (status will be "verified").
        """
        body: dict[str, Any] = {"code": code}
        data = await self._request(
            "POST", f"/v1/contacts/{contact_id}/verify", json=body
        )
        return VerifiedContact.model_validate(data)

    async def delete(self, contact_id: str) -> dict[str, Any]:
        """Delete a contact.

        Args:
            contact_id: The contact ID.

        Returns:
            Confirmation of deletion.
        """
        data = await self._request("DELETE", f"/v1/contacts/{contact_id}")
        return data

    async def update(
        self,
        contact_id: str,
        *,
        display_label: str | None = None,
        is_primary: bool | None = None,
    ) -> VerifiedContact:
        """Update a contact.

        Args:
            contact_id: The contact ID.
            display_label: Optional new display label.
            is_primary: Optional flag to set as primary contact.

        Returns:
            The updated verified contact.
        """
        body: dict[str, Any] = {}
        if display_label is not None:
            body["display_label"] = display_label
        if is_primary is not None:
            body["is_primary"] = is_primary
        data = await self._request("PATCH", f"/v1/contacts/{contact_id}", json=body)
        return VerifiedContact.model_validate(data)

    async def resend_otp(self, contact_id: str) -> VerifiedContact:
        """Resend the verification code for a pending contact.

        Args:
            contact_id: The contact ID.

        Returns:
            The contact (status remains "pending").
        """
        data = await self._request("POST", f"/v1/contacts/{contact_id}/resend")
        return VerifiedContact.model_validate(data)
