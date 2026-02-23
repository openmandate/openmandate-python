"""OpenMandate Python SDK — programmatic access to OpenMandate."""

from ._client import AsyncOpenMandate, OpenMandate
from ._exceptions import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    InternalServerError,
    NotFoundError,
    OpenMandateError,
    PermissionDeniedError,
    RateLimitError,
    ValidationError,
)
from ._pagination import AsyncPage, SyncPage
from ._version import __version__
from .types import (
    AnswerParam,
    CloseReason,
    Compatibility,
    Concern,
    Contact,
    ContactParam,
    CorrectionParam,
    IntakeAnswer,
    Mandate,
    MandateCreateParams,
    MandateListParams,
    MandateStatus,
    MandateSubmitAnswersParams,
    Match,
    MatchListParams,
    MatchStatus,
    Question,
    QuestionConstraints,
    QuestionOption,
    Strength,
)

__all__ = [
    # Client
    "AsyncOpenMandate",
    "OpenMandate",
    # Exceptions
    "APIConnectionError",
    "APIError",
    "APITimeoutError",
    "AuthenticationError",
    "BadRequestError",
    "ConflictError",
    "InternalServerError",
    "NotFoundError",
    "OpenMandateError",
    "PermissionDeniedError",
    "RateLimitError",
    "ValidationError",
    # Pagination
    "AsyncPage",
    "SyncPage",
    # Version
    "__version__",
    # Types
    "AnswerParam",
    "CloseReason",
    "Compatibility",
    "Concern",
    "Contact",
    "ContactParam",
    "CorrectionParam",
    "IntakeAnswer",
    "Mandate",
    "MandateCreateParams",
    "MandateListParams",
    "MandateStatus",
    "MandateSubmitAnswersParams",
    "Match",
    "MatchListParams",
    "MatchStatus",
    "Question",
    "QuestionConstraints",
    "QuestionOption",
    "Strength",
]
