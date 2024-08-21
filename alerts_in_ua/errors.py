"""Exception types definitions raises by `alerts-in-ua` API"""

import warnings
from functools import wraps

from typing_extensions import Optional


class ApiError(RuntimeError):
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"{message}")


class UnauthorizedError(ApiError):

    def __init__(self, message: Optional[str]) -> None:
        super().__init__(message or "Unauthorized: Incorrect token")


class RateLimitError(ApiError):

    def __init__(self, message: Optional[str]) -> None:
        super().__init__(message or "Too many requests: Rate limit exceeded")


class InternalServerError(ApiError):

    def __init__(self, message: Optional[str]) -> None:
        super().__init__(message or "Internal server error")


class ForbiddenError(ApiError):

    def __init__(self, message: Optional[str]) -> None:
        super().__init__(
            message or "Forbidden. API may not be available in some regions. "
                       "Please ask api@alerts.in.ua for details."
        )


def deprecation_warning(message: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__}:\n{message}",
                category=DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator


__all__ = (
    'deprecation_warning',
    'ApiError',
    'UnauthorizedError',
    'RateLimitError',
    'InternalServerError',
    'ForbiddenError',
)
