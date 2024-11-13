from typing import List

from fastapi import APIRouter, Depends

from model.request.knowledge_file_request import KnowledgeFileCreateRequest
from model.response_model import ResponseModel
from services.knowledge.knowledge_file_service import KnowledgeFileService

router = APIRouter()

"""
    知识库文件关联API
    1. 创建知识库文件关联
    2. 根据知识库id获取文件信息
    3. 删除知识库文件关联
"""


@router.post("/knowledge_file", response_model=ResponseModel, status_code=201)
def create_knowledge(knowledge_file_relations: List[KnowledgeFileCreateRequest],
                     service: KnowledgeFileService = Depends(KnowledgeFileService)):
    return ResponseModel.ok(service.batch_create_knowledge_file_relation(knowledge_file_relations))


@router.get("/knowledge_file/{knowledge_id}", response_model=ResponseModel, status_code=200)
def find_file_by_knowledge_id(knowledge_id: int, service: KnowledgeFileService = Depends(KnowledgeFileService)):
    return ResponseModel.ok(service.find_file_by_knowledge_id(knowledge_id))


@router.delete("/knowledge_file/{file_id}", response_model=ResponseModel, status_code=200)
def remove_knowledge_file_relation(file_id: int, service: KnowledgeFileService = Depends(KnowledgeFileService)):
    return ResponseModel.ok(service.remove_knowledge_file(file_id))
