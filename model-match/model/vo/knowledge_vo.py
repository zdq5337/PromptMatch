from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

from model.vo.file_vo import FileVO


class KnowledgeVO(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    creator: Optional[str] = None
    creator_id: Optional[str] = None
    create_time: Optional[datetime] = None
    modifier: Optional[str] = None
    modifier_id: Optional[str] = None
    update_time: Optional[datetime] = None
    file_vos: Optional[List[FileVO]] = None

    class Config:
        orm_mode = True  # 允许Pydantic模型直接从ORM模型实例化
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S')
        }
