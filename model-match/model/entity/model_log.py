from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class ModelLog(SQLModel, table=True):
    __tablename__ = "model_log"

    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True}, description="主键id")
    model_name: str = Field(nullable=False, max_length=255, description="模型名称")
    model_source: str = Field(nullable=False, max_length=255, description="模型来源")
    question: str = Field(nullable=False, description="问题")
    answer: str = Field(nullable=False, description="答案")
    document: Optional[str] = Field(default=None, description="匹配到的文档")
    create_time: datetime = Field(default_factory=datetime.now, nullable=False, description="创建时间")

    class Config:
        orm_mode = True

    # 当创建新实例时自动设置 create_time 和 update_time
    def __init__(self, **data):
        super().__init__(**data)
        if self.id is None:
            self.create_time = datetime.now()