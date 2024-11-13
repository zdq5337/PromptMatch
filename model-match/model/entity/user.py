'''
Description: 用户实体
Author: Kyeoni hujr
Date: 2024-09-02 14:53:38
LastEditors: Kyeoni hujr
LastEditTime: 2024-09-06 14:56:24
'''
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field
from datetime import datetime

class Role(str, Enum):
  ADMIN = "admin"
  USER = "user"

# 定义模型
class User(SQLModel, table=True):
  # 指定数据库表的名称
  __tablename__ = "user"

  id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True}, description="主键id")
  username: str = Field(index=True, unique=True, nullable=False, max_length=50, description="用户名")
  password: str = Field(nullable=False, max_length=128, description="密码")
  role: str = Field(default=Role.USER.value, nullable=False, description="用户角色")
  create_time: datetime = Field(default_factory=datetime.now, nullable=False, description="创建时间")
  last_login_time: datetime | None = Field(default_factory=datetime.now, nullable=False, description="最后登录时间")


# CREATE TABLE user (
#     id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(50) NOT NULL UNIQUE,
#     password VARCHAR(128) NOT NULL,
#     create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     last_login_time DATETIME,
#     role VARCHAR(10) NOT NULL
# );