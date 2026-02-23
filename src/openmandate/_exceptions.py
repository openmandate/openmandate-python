from __future__ import annotations

from typing import Any


class OpenMandateError(Exception):
    """Base exception for all OpenMandate SDK errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class APIError(OpenMandateError):
    """Raised when the API returns an error response."""

    status_code: int
    code: str | None
    details: list[dict[str, Any]] | None

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        code: str | None = None,
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.details = details

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"status_code={self.status_code}, "
            f"code={self.code!r})"
        )


class BadRequestError(APIError):
    """Raised on 400 Bad Request responses (validation errors)."""

    def __init__(
        self,
        message: str = "The request was invalid.",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, status_code=400, **kwargs)


class AuthenticationError(APIError):
    """Raised on 401 Unauthorized responses."""

    def __init__(
        self,
        message: str = "Invalid API key or missing authentication.",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, status_code=401, **kwargs)


class PermissionDeniedError(APIError):
    """Raised on 403 Forbidden responses."""

    def __init__(
        self,
        message: str = "You don't have permission to access this resource.",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, status_code=403, **kwargs)


class NotFoundError(APIError):
    """Raised on 404 Not Found responses."""

    def __init__(
        self,
        message: str = "The requested resource was not found.",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, status_code=404, **kwargs)


class ConflictError(APIError):
    """Raised on 409 Conflict responses."""

    def __init__(
        self,
        message: str = "The request conflicts with the current state of the resource.",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, status_code=409, **kwargs)


class ValidationError(APIError):
    """Raised on 422 Unprocessable Entity responses."""

    def __init__(
        self,
        message: str = "The request body failed validation.",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, status_code=422, **kwargs)


class RateLimitError(APIError):
    """Raised on 429 Too Many Requests responses."""

    def __init__(
        self,
        message: str = "Rate limit exceeded. Please slow down.",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, status_code=429, **kwargs)


class InternalServerError(APIError):
    """Raised on 5xx responses."""

    def __init__(
        self,
        message: str = "The server encountered an internal error.",
        **kwargs: Any,
    ) -> None:
        super().__init__(message, status_code=kwargs.pop("status_code", 500), **kwargs)


class APIConnectionError(OpenMandateError):
    """Raised when the SDK cannot connect to the API."""

    def __init__(
        self,
        message: str = "Failed to connect to the OpenMandate API.",
    ) -> None:
        super().__init__(message)


class APITimeoutError(APIConnectionError):
    """Raised when a request times out."""

    def __init__(
        self,
        message: str = "Request to the OpenMandate API timed out.",
    ) -> None:
        super().__init__(message)


STATUS_CODE_TO_EXCEPTION: dict[int, type[APIError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: ValidationError,
    429: RateLimitError,
}


def _make_api_error(status_code: int, body: dict[str, Any] | None) -> APIError:
    """Create the appropriate exception from an HTTP status code and response body."""
    error_body = (body or {}).get("error", {})
    message = error_body.get("message", f"HTTP {status_code} error")
    code = error_body.get("code")
    details = error_body.get("details")

    exc_class = STATUS_CODE_TO_EXCEPTION.get(status_code)
    if exc_class is not None:
        return exc_class(message=message, code=code, details=details)

    if status_code >= 500:
        return InternalServerError(
            message=message, status_code=status_code, code=code, details=details
        )

    return APIError(
        message=message, status_code=status_code, code=code, details=details
    )
