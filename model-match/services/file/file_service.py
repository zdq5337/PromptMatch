from typing import Optional

from utils.aliyun_oss import upload_file_to_oss, get_oss_file_url
from utils.logger import logger


class FileService:
    def __init__(self):
        pass

    def upload_file(self, file_data: bytes, file_name: str) -> Optional[str]:
        logger.info(f"services/file/file_service.py upload_file file_name: {file_name}")
        file_url = upload_file_to_oss(file_data, file_name)
        if file_url:
            return file_url
        else:
            return None

    def get_file_url(self, file_path: str) -> Optional[str]:
        logger.info(f"services/file/file_service.py get_file_url file_path: {file_path}")
        file_url = get_oss_file_url(file_path)
        if file_url:
            return file_url
        else:
            return None
