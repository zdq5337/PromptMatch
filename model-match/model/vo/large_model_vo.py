from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LargeModelVO(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    token: Optional[int] = None
    company: Optional[str] = None
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
