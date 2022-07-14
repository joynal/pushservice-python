from starlette.exceptions import HTTPException as StarletteHTTPException


class ApiException(StarletteHTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code, detail)
