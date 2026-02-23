from __future__ import annotations

from pydantic import BaseModel


class Contact(BaseModel):
    """Contact information for a mandate owner or match counterparty."""

    email: str | None = None
    telegram: str | None = None
    whatsapp: str | None = None
    phone: str | None = None


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
