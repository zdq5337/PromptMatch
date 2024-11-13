from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


# 定义模型
class Knowledge(SQLModel, table=True):
    # 指定数据库表的名称
    __tablename__ = "knowledge"

    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True}, description="主键id")
    name: str = Field(nullable=False, max_length=63, description="知识库名称")
    description: str = Field(nullable=False, max_length=255, description="知识库描述")
    icon: str = Field(nullable=False, max_length=63, description="知识库图标")
    deleted: bool = Field(default=False, nullable=False, description="是否已删除：0-未删除；1-已删除")
    creator: str = Field(default='', nullable=False, max_length=32, description="创建人")
    creator_id: str = Field(default='', nullable=False, max_length=32, description="创建人id")
    create_time: datetime = Field(default_factory=datetime.now, nullable=False, description="创建时间")
    modifier: str = Field(default='', nullable=False, max_length=64, description="更新人")
    modifier_id: str = Field(default='', nullable=False, max_length=32, description="更新id")
    update_time: datetime = Field(default_factory=datetime.now, nullable=False,
                                  description="更新时间")

    class Config:
        orm_mode = True

    # 当创建新实例时自动设置 create_time 和 update_time
    def __init__(self, **data):
        super().__init__(**data)
        if self.id is None:
            self.create_time = datetime.now()
            self.deleted = False
            self.creator = "admin"
            self.creator_id = "000001"
        self.update_time = datetime.now()
        self.modifier = "admin"
        self.modifier_id = "000001"