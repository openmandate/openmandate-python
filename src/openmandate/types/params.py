from __future__ import annotations

from typing import TypedDict

from typing_extensions import NotRequired


class MandateCreateParams(TypedDict):
    """Parameters for creating a new mandate."""

    want: str
    offer: str


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


class AddContactParams(TypedDict):
    """Parameters for adding a new contact."""

    contact_type: str
    contact_value: str
    display_label: NotRequired[str]


class VerifyContactParams(TypedDict):
    """Parameters for verifying a contact."""

    code: str


class UpdateContactParams(TypedDict, total=False):
    """Parameters for updating a contact."""

    display_label: str
    is_primary: bool
