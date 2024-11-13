from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FileVO(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    oss_path: Optional[str] = None
    size: Optional[int] = None
    knowledge_id: Optional[int] = None
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


class FileUrlVO(BaseModel):
    file_url: Optional[str] = None

    class Config:
        orm_mode = True  # 允许Pydantic模型直接从ORM模型实例化
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S')
        }


class FilePathVO(BaseModel):
    oss_path: Optional[str] = None

    class Config:
        orm_mode = True  # 允许Pydantic模型直接从ORM模型实例化
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S')
        }
