from typing import List, Dict, Any

from fastapi import Depends
from sqlmodel import Session

from constants.large_model_enum import get_all_model_name
from services.database.base import get_session
from utils.logger import logger


class LargeModelService:
    def __init__(self,
                 session: Session = Depends(get_session)):
        self.session = session

    def get_all_large_models(self) -> list[dict[str, Any]]:
        all_model_name = get_all_model_name()
        logger.info(
            f"model-match services:large_model:LargeModelService:get_all_large_models large_models: {all_model_name}")
        return all_model_name
