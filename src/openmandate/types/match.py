from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .shared import Compatibility, Contact


MatchStatus = Literal["pending", "accepted", "confirmed", "declined", "closed", "expired"]

MatchOutcome = Literal["succeeded", "ongoing", "failed"]


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
    outcome: str | None = None
    outcome_at: str | None = None
    show_outcome_prompt: bool = False
    force_final_outcome: bool = False
