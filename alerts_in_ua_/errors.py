import warnings
from functools import wraps


class ApiError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(f"{message}")


class UnauthorizedError(ApiError):
    pass


class RateLimitError(ApiError):
    pass


class InternalServerError(ApiError):
    pass


class ForbiddenError(ApiError):
    pass


class InvalidParameterException(Exception):
    pass


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
