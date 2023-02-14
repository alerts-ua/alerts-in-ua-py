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