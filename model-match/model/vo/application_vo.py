from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from model.vo.knowledge_vo import KnowledgeVO


class ApplicationVO(BaseModel):
    id: Optional[int] = None
    model_name: Optional[str] = None
    model_name_valid: Optional[bool] = False
    knowledge_vos: Optional[List[KnowledgeVO]] = []
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    creator: Optional[str] = None
    creator_id: Optional[str] = None
    create_time: Optional[datetime] = None
    modifier: Optional[str] = None
    modifier_id: Optional[str] = None
    update_time: Optional[datetime] = None

    class Config:
        orm_mode = True  # 允许Pydantic模型直接从ORM模型实例化
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S')
        }
