from fastapi import status

from src.core.exceptions import CustomHTTPException


class PartRequestNotFound(CustomHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Partisipation request not found'


class AlreadyRequested(CustomHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Already requested partisipation'


class NotNewPartRequest(CustomHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Action avaliable only to new partisipation requests'
