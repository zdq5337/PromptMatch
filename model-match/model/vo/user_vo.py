'''
Description: 用户
Author: Kyeoni hujr
Date: 2024-09-02 15:34:35
LastEditors: Kyeoni hujr
LastEditTime: 2024-09-10 17:29:12
'''

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from model.entity.user import Role


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    role: Role
    create_time: datetime
    last_login_time: datetime
    username: str = Field(..., max_length=10, example="用户名")
    access_token: str | None = Field(None, example="访问令牌")
    token_type: str | None = Field(None, example="令牌类型")


class User(UserRead):
    pass
