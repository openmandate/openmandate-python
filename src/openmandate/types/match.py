from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .shared import Compatibility, Contact


MatchStatus = Literal["pending", "accepted", "confirmed", "declined", "closed"]


class Match(BaseModel):
    """A match between two mandates on OpenMandate."""

    id: str
    status: MatchStatus
    mandate_id: str
    created_at: str
    responded_at: str | None = None
    confirmed_at: str | None = None
    compatibility: Compatibility | None = None
    contact: Contact | None = None
