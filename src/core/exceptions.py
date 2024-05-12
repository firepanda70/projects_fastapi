from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Custom HTTP exception'
    headers = None

    def __init__(self) -> None:
        super().__init__(self.status_code, self.detail, self.headers)


class ServerError(CustomHTTPException):
    detail = 'Server error'
