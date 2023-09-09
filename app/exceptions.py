from fastapi import HTTPException, status


class NoDatabaseConnection(HTTPException):
    def __init__(self, detail=None):
        super(HTTPException, self).__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail or "No database connection"
        )


class UserAlreadyExsitsException(HTTPException):
    def __init__(self, detail=None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail or 'User already exists',
        )


class InvalidEmailOrPasswordException(HTTPException):
    def __init__(self, detail=None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail or "Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserIsNotPresentedException(HTTPException):
    def __init__(self, detail=None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail or "User is not presented",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidTokenFormatException(HTTPException):
    def __init__(self, detail=None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail or "Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenExpiredException(HTTPException):
    def __init__(self, detail=None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail or "Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenAbsentException(HTTPException):
    def __init__(self, detail=None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail or "No token",
            headers={"WWW-Authenticate": "Bearer"},
        )


class GetErrorFromBlackbox(Exception):
    pass
