from fastapi import status

from src.core.exceptions import CustomHTTPException


class Forbidden(CustomHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Not enough rights'


class GroupNameTaken(CustomHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Group name already in use'


class GroupNotFound(CustomHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Group not found'


class FrozenGroup(CustomHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Frozen group cannot be changed'


class PartisipantAlreadyInGroup(CustomHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Patisipant already in group'


class PartisipantNotInGroup(CustomHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Patisipant not in group'


class OwnerPartisipantSupergroup(CustomHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Supergroup cannot be revoked from owner partisipant'
