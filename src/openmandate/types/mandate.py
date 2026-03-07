from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from .shared import IntakeAnswer, Question


MandateStatus = Literal[
    "intake", "processing", "active", "pending_input", "matched", "closed"
]

CloseReason = Literal["user_closed", "matched"]


class Mandate(BaseModel):
    """A mandate on OpenMandate."""

    id: str
    status: MandateStatus
    category: str | None = None
    created_at: str
    closed_at: str | None = None
    close_reason: CloseReason | None = None
    expires_at: str | None = None
    source: str | None = None
    summary: str | None = None
    match_id: str | None = None
    contact_ids: list[str] = []
    pending_questions: list[Question] = []
    intake_answers: list[IntakeAnswer] = []
