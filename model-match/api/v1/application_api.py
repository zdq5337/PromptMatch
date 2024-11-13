from fastapi import APIRouter, Depends

from model.response_model import ResponseModel
from model.request.application_request import ApplicationCreateRequest, ApplicationEditRequest
from services.application.application_service import ApplicationService

router = APIRouter()

"""
    应用管理API
    1. 获取所有应用信息
    2. 创建应用
    3. 更新应用
"""

@router.get("/application", response_model=ResponseModel)
def get_all_knowledge(service: ApplicationService = Depends(ApplicationService)):
    return ResponseModel.ok(service.get_all_applications())

@router.get("/application/{application_id}", response_model=ResponseModel)
def get_knowledge_by_id(application_id: int, service: ApplicationService = Depends(ApplicationService)):
    return ResponseModel.ok(service.get_application_by_id(application_id))


@router.post("/application", response_model=ResponseModel, status_code=201)
def create_knowledge(application_create_request: ApplicationCreateRequest,
                     service: ApplicationService = Depends(ApplicationService)):
    return ResponseModel.ok(service.create_application(application_create_request))


@router.put("/application", response_model=ResponseModel)
def update_knowledge(application_edit_request: ApplicationEditRequest,
                     service: ApplicationService = Depends(ApplicationService)):
    return ResponseModel.ok(service.update_application(application_edit_request))
