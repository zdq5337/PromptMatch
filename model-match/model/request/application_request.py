from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, validator


class ApplicationCreateRequest(BaseModel):
    name: str = Field(..., max_length=63, example="应用名称", description="应用名称")
    description: Optional[str] = Field(None, max_length=255, example="应用描述", description="应用描述")
    icon: Optional[str] = Field(None, max_length=63, example="应用图标", description="应用图标")
    # 关联知识库id
    knowledge_id: Optional[int] = Field(None, example=1, description="关联知识库id")
    knowledge_ids: Optional[List[int]] = Field(None, example=[1, 2], description="关联知识库id列表")
    # 关联的模型
    model_name: Optional[str] = Field(None, max_length=128, example="模型标识", description="关联模型标识")

    # ... 其他需要验证的字段 ...
    @validator('name', 'description', 'icon', 'model_name', pre=True)
    def check_not_empty(cls, value):
        if not value:
            raise ValueError("该字段不能为空")
        return value


class ApplicationEditRequest(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., max_length=63, example="应用名称", description="应用名称")
    description: Optional[str] = Field(None, max_length=255, example="应用描述", description="应用描述")
    icon: Optional[str] = Field(None, max_length=63, example="应用图标", description="应用图标")
    # 关联知识库id
    knowledge_id: Optional[int] = Field(None, example=1, description="关联知识库id")
    knowledge_ids: Optional[List[int]] = Field(None, example=[1, 2], description="关联知识库id列表")
    # 关联的模型
    # model_name: Optional[List[int]] = Field(None, description="关联模型标识")
    model_name: Optional[str] = Field(None, max_length=128, example="模型标识", description="模型标识")
    # 通用字段
    deleted: Optional[bool] = Field(None, example=False)
    creator: Optional[str] = Field(None, max_length=32, example="创建人")
    creator_id: Optional[str] = Field(None, max_length=32, example="创建人id")
    create_time: Optional[datetime] = Field(None, example=datetime.now())
    modifier: Optional[str] = Field(None, max_length=64, example="更新人")
    modifier_id: Optional[str] = Field(None, max_length=32, example="更新id")
    update_time: Optional[datetime] = Field(None, example=datetime.now())

    # ... 其他需要验证的字段 ...
    @validator('id', 'name', 'description', 'icon', pre=True)
    def check_not_empty(cls, value):
        if not value:
            raise ValueError("该字段不能为空")
        return value
