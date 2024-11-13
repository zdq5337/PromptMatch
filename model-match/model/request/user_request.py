import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserCreateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(..., max_length=10, example="用户名")
    password: str = Field(..., max_length=128, min_length=8, example="密码")

    @field_validator('username')
    def check_username(cls, value) -> str:
        if not re.match(r'^[A-Za-z\d_]{5,10}$', value):
            raise ValueError('用户名由字母数字下划线组成，长度为5-10位')
        return value

    @field_validator('password')
    def check_password(cls, value) -> str:
        if not re.match(
                r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()\_\-\+\\,.?":{}|<>])[A-Za-z\d!@#$%^&*()\_\-\+\\,.?":{}|<>]{8,}$',
                value):
            raise ValueError('密码必须包含字母、数字和特殊字符，长度不能小于8位')
        return value
