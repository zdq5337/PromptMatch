from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class KnowledgeFileCreateRequest(BaseModel):
    name: str = Field(..., max_length=63, examples=["文件名称"])
    oss_path: str = Field(..., max_length=511, examples=["文件oss路径"])
    # 关联知识库id
    knowledge_id: int = Field(..., examples=[1])
    size: int = Field(0, examples=["上传文件的大小，按照byte表示"])
    file_id: Optional[int] = Field(None, examples=[1])

    # ... 其他需要验证的字段 ...
    @validator('name', 'oss_path', 'knowledge_id', 'size', pre=True)
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
    @validator('id', 'name', 'description')
    def check_not_empty(cls, value):
        if not value:
            raise ValueError("该字段不能为空")
        return value
