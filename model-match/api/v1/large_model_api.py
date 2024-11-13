from fastapi import APIRouter, Depends

from model.response_model import ResponseModel
from services.application.large_model_service import LargeModelService

router = APIRouter()

"""
    大模型管理API
    1. 获取所有大模型信息
"""

@router.get("/large_model", response_model=ResponseModel)
def get_all_knowledge(service: LargeModelService = Depends(LargeModelService)):
    return ResponseModel.ok(service.get_all_large_models())
