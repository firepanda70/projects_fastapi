from fastapi import status

from src.core.exceptions import CustomHTTPException


class AlreadyPartisipant(CustomHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'User already partisipating'


class NotPartisipant(CustomHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'User not partisipant'


class PartisipantNotFound(CustomHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Partisipant not found'


class PartisipantIsOwner(CustomHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Owner cannot be deleted'
