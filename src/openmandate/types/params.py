from __future__ import annotations

from typing import TypedDict

from typing_extensions import NotRequired


class ContactParam(TypedDict):
    """Contact information for creating a mandate."""

    email: NotRequired[str]
    telegram: NotRequired[str]
    whatsapp: NotRequired[str]
    phone: NotRequired[str]


class MandateCreateParams(TypedDict):
    """Parameters for creating a new mandate."""

    category: str
    contact: NotRequired[ContactParam]


class AnswerParam(TypedDict):
    """A single answer to an intake question."""

    question_id: str
    value: str


class CorrectionParam(TypedDict):
    """A correction to a previously submitted answer."""

    question_id: str
    value: str


class MandateSubmitAnswersParams(TypedDict):
    """Parameters for submitting answers to intake questions."""

    answers: list[AnswerParam]
    corrections: NotRequired[list[CorrectionParam]]


class MandateListParams(TypedDict, total=False):
    """Parameters for listing mandates."""

    status: str
    limit: int
    next_token: str


class MatchListParams(TypedDict, total=False):
    """Parameters for listing matches."""

    limit: int
    next_token: str
