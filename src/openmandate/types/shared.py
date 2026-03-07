from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

ContactType = Literal["email"]
VerificationStatus = Literal["pending", "verified"]


class Contact(BaseModel):
    """Contact information revealed on mutual match accept."""

    email: str | None = None


class VerifiedContact(BaseModel):
    """A verified contact method belonging to the authenticated user."""

    id: str
    contact_type: str
    contact_value: str
    display_label: str
    status: str
    is_primary: bool
    verified_at: str | None = None
    created_at: str


class QuestionOption(BaseModel):
    """A selectable option for single_select or multi_select questions."""

    value: str
    label: str


class QuestionConstraints(BaseModel):
    """Validation constraints for a question answer."""

    min_length: int | None = None
    max_length: int | None = None


class Question(BaseModel):
    """A pending intake question to be answered."""

    id: str
    text: str
    type: str
    required: bool
    options: list[QuestionOption] | None = None
    constraints: QuestionConstraints | None = None
    allow_custom: bool = False


class IntakeAnswer(BaseModel):
    """A previously submitted answer in the intake flow."""

    question_id: str
    question_text: str
    value: str
    question_type: str
    question_options: list[QuestionOption] | None = None


class Strength(BaseModel):
    """A compatibility strength between two mandates."""

    label: str
    description: str


class Concern(BaseModel):
    """A compatibility concern between two mandates."""

    label: str
    description: str


class Compatibility(BaseModel):
    """Compatibility assessment for a match."""

    score: int
    summary: str
    strengths: list[Strength] = []
    concerns: list[Concern] = []
