from fastapi import APIRouter, Depends

from model.response_model import ResponseModel
from model.request.knowledge_request import KnowledgeCreateRequest, KnowledgeEditRequest
from services.knowledge.knowledge_service import KnowledgeService

router = APIRouter()


"""
    知识库管理API
    1. 获取所有知识库信息
    2. 根据id获取知识库信息
    3. 创建知识库
    4. 更新知识库
"""

@router.get("/knowledge", response_model=ResponseModel)
def get_all_knowledge(service: KnowledgeService = Depends(KnowledgeService)):
    return ResponseModel.ok(service.get_all_knowledge())


@router.get("/knowledge/{knowledge_id}", response_model=ResponseModel)
def get_knowledge_by_id(knowledge_id: int, service: KnowledgeService = Depends(KnowledgeService)):
    return ResponseModel.ok(service.get_knowledge_by_id(knowledge_id))


@router.post("/knowledge", response_model=ResponseModel, status_code=201)
def create_knowledge(knowledge_create_request: KnowledgeCreateRequest,
                     service: KnowledgeService = Depends(KnowledgeService)):
    return ResponseModel.ok(service.create_knowledge(knowledge_create_request))


@router.put("/knowledge", response_model=ResponseModel)
def update_knowledge(knowledge_edit_request: KnowledgeEditRequest,
                     service: KnowledgeService = Depends(KnowledgeService)):
    return ResponseModel.ok(service.update_knowledge(knowledge_edit_request))


@router.delete("/knowledge/{knowledge_id}", response_model=ResponseModel)
def delete_knowledge(knowledge_id: int, service: KnowledgeService = Depends(KnowledgeService)):
    return ResponseModel.ok(service.delete_knowledge(knowledge_id))
