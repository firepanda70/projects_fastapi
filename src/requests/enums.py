from enum import Enum


class RequestStatus(str, Enum):
    NEW = 'NEW'
    ACCEPTED = 'ACCEPTED'
    DENIED = 'DENIED'
