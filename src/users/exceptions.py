from fastapi import status

from src.core.exceptions import CustomHTTPException


class InvalidCredentials(CustomHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Ivalid username or password'


class UsernameTaken(CustomHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Username already taken'


class NotAuthorized(CustomHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid token'
