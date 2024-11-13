from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class KnowledgeCreateRequest(BaseModel):
    name: str = Field(..., max_length=63, example="知识库名称")
    description: str = Field(..., max_length=255, example="知识库描述")
    icon: Optional[str] = Field(None, max_length=63, example="知识库图标")

    # ... 其他需要验证的字段 ...
    @validator('name', 'description')
    def check_not_empty(cls, value):
        if not value:
            raise ValueError("该字段不能为空")
        return value


class KnowledgeEditRequest(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., max_length=63, example="知识库名称")
    description: str = Field(..., max_length=255, example="知识库描述")
    icon: Optional[str] = Field(None, max_length=63, example="知识库图标")
    deleted: Optional[bool] = Field(None, example=False)
    creator: Optional[str] = Field(None, max_length=32, example="创建人")
    creator_id: Optional[str] = Field(None, max_length=32, example="创建人id")
    create_time: Optional[datetime] = Field(None, example=datetime.now())
    modifier: Optional[str] = Field(None, max_length=64, example="更新人")
    modifier_id: Optional[str] = Field(None, max_length=32, example="更新id")
    update_time: Optional[datetime] = Field(None, example=datetime.now())

    # ... 其他需要验证的字段 ...
    @validator('name', 'id', 'name', 'description')
    def check_not_empty(cls, value):
        if not value:
            raise ValueError("该字段不能为空")
        return value
