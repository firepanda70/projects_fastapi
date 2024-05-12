from fastapi import status

from src.core.exceptions import CustomHTTPException


class ProjectNotFound(CustomHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Project not found'
