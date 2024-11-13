from datetime import datetime
from pydantic import BaseModel
from typing import Any, Optional


class ResponseModel(BaseModel):
    code: str
    message: str
    data: Optional[Any] = None
    timestamp: int

    @staticmethod
    def format_response(data=None, code='000000', message='请求成功！'):
        timestamp = int(datetime.now().timestamp() * 1000)  # 获取当前时间戳（毫秒级）
        return ResponseModel(code=code, message=message, data=data, timestamp=timestamp)

    @staticmethod
    def ok(data=None):
        return ResponseModel.format_response(data)

    @staticmethod
    def fail(code='999999', message='请求失败！'):
        return ResponseModel.format_response(code=code, message=message)

    @staticmethod
    def custom(code='000000', message='请求成功！', data=None):
        return ResponseModel.format_response(data=data, code=code, message=message)
