class ErrorCode:
    INTERNAL_SERVER_ERROR = 500, "服务内部错误，请联系管理员"


class ApiException(Exception):
    REQUEST_FAILED_CODE = "999999"

    def __init__(self, message=None, code=None, http_code=None, cause=None):
        self.message = message if message else ErrorCode.INTERNAL_SERVER_ERROR[1]
        self.code = code if code else self.REQUEST_FAILED_CODE
        self.http_code = http_code if http_code else ErrorCode.INTERNAL_SERVER_ERROR[0]
        self.cause = cause

    @property
    def get_http_code(self):
        return self.http_code

    @property
    def get_code(self):
        return self.code

    @property
    def get_message(self):
        return self.message

    def __str__(self):
        return f"ApiException: {self.code}, {self.http_code}, {self.args}"
