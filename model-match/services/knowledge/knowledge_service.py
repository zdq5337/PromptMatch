from typing import List

from fastapi import Depends, HTTPException
from sqlmodel import Session

from model.entity.knowledge import Knowledge
from model.request.knowledge_file_request import KnowledgeEditRequest
from model.request.knowledge_request import KnowledgeCreateRequest
from model.vo.file_vo import FileVO
from model.vo.knowledge_vo import KnowledgeVO
from repository.file_repository import FileRepository
from repository.knowledge_file_relation_repository import KnowledgeFileRelationRepository
from repository.knowledge_repository import KnowledgeRepository
from services.database.base import get_session
from utils.aliyun_oss import get_oss_file_url
from utils.json_converter import JsonConverter
from utils.logger import logger


class KnowledgeService:
    def __init__(self, knowledge_repo: KnowledgeRepository = Depends(KnowledgeRepository),
                 knowledge_file_relation_repo: KnowledgeFileRelationRepository = Depends(
                     KnowledgeFileRelationRepository),
                 file_repo: FileRepository = Depends(FileRepository),
                 session: Session = Depends(get_session)):
        self.knowledge_repo = knowledge_repo
        self.knowledge_file_relation_repo = knowledge_file_relation_repo
        self.file_repo = file_repo
        self.session = session

    def get_all_knowledge(self) -> List[KnowledgeVO]:
        knowledges = self.knowledge_repo.get_all_knowledge(self.session)
        logger.info(
            f"model-match services:knowledge:KnowledgeService:get_all_knowledge knowledges: {JsonConverter.to_json(knowledges)}")
        return [KnowledgeVO.model_validate(knowledge) for knowledge in knowledges]

    def get_knowledge_by_id(self, knowledge_id: int) -> KnowledgeVO:
        knowledge = self.knowledge_repo.get_knowledge_by_id(knowledge_id, self.session)
        logger.info(
            f"model-match services:knowledge:KnowledgeService:get_knowledge_by_id knowledge: {JsonConverter.to_json(knowledge)}")
        if knowledge:
            knowledge_vo = KnowledgeVO.model_validate(knowledge)
            knowledge_file_relations = self.knowledge_file_relation_repo.get_knowledge_file_relation_by_knowledge_id(
                knowledge_id,
                self.session)
            logger.info(
                f"model-match services:knowledge:KnowledgeService:get_knowledge_by_id knowledge_file_relations: {JsonConverter.to_json(knowledge_file_relations)}")
            file_ids = [relation.file_id for relation in knowledge_file_relations]
            files = self.file_repo.get_files_by_ids(file_ids, self.session)
            logger.info(
                f"model-match services:knowledge:KnowledgeService:get_knowledge_by_id files: {JsonConverter.to_json(files)}")
            for file in files:
                file.oss_path = get_oss_file_url(file.oss_path)
            knowledge_vo.file_vos = [FileVO.model_validate(file) for file in files]
            return knowledge_vo
        else:
            raise HTTPException(status_code=404, detail="Knowledge not found")

    def create_knowledge(self, knowledge_create_request: KnowledgeCreateRequest, ) -> KnowledgeVO:
        # 将验证后的数据转换为Knowledge模型
        knowledge = Knowledge(**knowledge_create_request.model_dump())
        logger.info(
            f"model-match services:knowledge:KnowledgeService:create_knowledge knowledge: {JsonConverter.to_json(knowledge)}")
        knowledge = self.knowledge_repo.create_knowledge(knowledge, self.session)
        self.session.commit()
        self.session.refresh(knowledge)
        return KnowledgeVO.model_validate(knowledge)

    def update_knowledge(self, knowledge_edit_request: KnowledgeEditRequest) -> KnowledgeVO:
        # 将验证后的数据转换为Knowledge模型
        new_knowledge = Knowledge(**knowledge_edit_request.model_dump())
        logger.info(
            f"model-match services:knowledge:KnowledgeService:update_knowledge new_knowledge: {JsonConverter.to_json(new_knowledge)}")
        old_knowledge = self.knowledge_repo.get_knowledge_by_id(new_knowledge.id, self.session)
        logger.info(
            f"model-match services:knowledge:KnowledgeService:update_knowledge old_knowledge: {JsonConverter.to_json(old_knowledge)}")
        if old_knowledge:
            knowledge = self.knowledge_repo.update_knowledge(new_knowledge, old_knowledge, self.session)
            self.session.commit()
            self.session.refresh(old_knowledge)
            return KnowledgeVO.model_validate(knowledge)
        else:
            raise HTTPException(status_code=404, detail="Knowledge not found")

    def delete_knowledge(self, knowledge_id: int) -> KnowledgeVO:
        knowledge = self.knowledge_repo.get_knowledge_by_id(knowledge_id, self.session)
        logger.info(
            f"model-match services:knowledge:KnowledgeService:delete_knowledge knowledge: {JsonConverter.to_json(knowledge)}")
        if knowledge:
            knowledge = self.knowledge_repo.delete_knowledge(knowledge, self.session)
            self.session.commit()
            self.session.refresh(knowledge)
            logger.info(
                f"model-match services:knowledge:KnowledgeService:delete_knowledge knowledge: {JsonConverter.to_json(knowledge)}")
            return KnowledgeVO.model_validate(knowledge)
        else:
            raise HTTPException(status_code=404, detail="Knowledge not found")
