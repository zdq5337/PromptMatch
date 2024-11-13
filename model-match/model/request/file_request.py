from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class FileUploadRequest(BaseModel):
    file_path: str = Field(..., max_length=511, example="文件路径前缀")