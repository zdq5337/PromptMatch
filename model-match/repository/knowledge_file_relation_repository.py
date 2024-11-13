from model.entity.file import File
from model.entity.knowledge import Knowledge
from fastapi import HTTPException, Depends
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime

from model.entity.knowledge_file_relation import KnowledgeFileRelation
from services.database.base import get_session


class KnowledgeFileRelationRepository:

    def get_knowledge_file_relation_by_id(self, knowledge_file_relation_id: int, session: Session) -> Optional[
        KnowledgeFileRelation]:
        return session.query(KnowledgeFileRelation).filter(KnowledgeFileRelation.id == knowledge_file_relation_id,
                                                           KnowledgeFileRelation.deleted.is_(False)).first()

    def get_knowledge_file_relation_by_file_id(self, file_id: int, session: Session) -> List[KnowledgeFileRelation]:
        return session.query(KnowledgeFileRelation).filter(KnowledgeFileRelation.file_id == file_id,
                                                           KnowledgeFileRelation.deleted.is_(False)).all()

    def get_knowledge_file_relation_by_knowledge_id(self, knowledge_id: int, session: Session) -> List[
        KnowledgeFileRelation]:
        return session.query(KnowledgeFileRelation).filter(KnowledgeFileRelation.knowledge_id == knowledge_id,
                                                           KnowledgeFileRelation.deleted.is_(False)).all()

    def get_knowledge_file_relation_count_by_knowledge_id(self, knowledge_id: int, session: Session) -> List[
        KnowledgeFileRelation]:
        return session.query(KnowledgeFileRelation).filter(KnowledgeFileRelation.knowledge_id == knowledge_id,
                                                           KnowledgeFileRelation.deleted.is_(False)).count()

    def get_all_knowledge_file_relations(self, session: Session) -> List[KnowledgeFileRelation]:
        return session.query(KnowledgeFileRelation).filter(KnowledgeFileRelation.deleted.is_(False)).all()

    def create_knowledge_file_relation(self, knowledge_file_relation: KnowledgeFileRelation,
                                       session: Session) -> KnowledgeFileRelation:
        session.add(knowledge_file_relation)
        return knowledge_file_relation

    def update_knowledge_file_relation(self, knowledge_file_relation_id: int,
                                       new_knowledge_file_relation: KnowledgeFileRelation,
                                       session: Session) -> KnowledgeFileRelation:
        old_knowledge_file_relation = self.get_knowledge_file_relation_by_id(knowledge_file_relation_id)
        if old_knowledge_file_relation:
            for key, value in new_knowledge_file_relation.model_dump().items():
                setattr(old_knowledge_file_relation, key, value)
            session.commit()
            return old_knowledge_file_relation
        else:
            raise HTTPException(status_code=404, detail="KnowledgeFileRelation not found")

    def delete_knowledge_file_relation(self, knowledge_file_relation: KnowledgeFileRelation,
                                       session: Session) -> KnowledgeFileRelation:
        knowledge_file_relation.deleted = True  # 逻辑删除
        knowledge_file_relation.update_time = datetime.now()  # 更新时间
        return knowledge_file_relation

    def batch_create_knowledge_file_relations(self, knowledge_file_relations: List[KnowledgeFileRelation],
                                              session: Session) -> List[
        KnowledgeFileRelation]:
        for relation in knowledge_file_relations:
            session.add(relation)
        session.commit()
        return knowledge_file_relations

    def batch_delete_knowledge_file_relations(self, knowledge_file_relation_ids: List[int], session: Session) -> List[
        KnowledgeFileRelation]:
        existing_relations = {relation.id for relation in self.get_all_knowledge_file_relations()}
        non_existing_or_deleted_ids = [id for id in knowledge_file_relation_ids if id not in existing_relations]

        if non_existing_or_deleted_ids:
            raise HTTPException(status_code=404,
                                detail=f"KnowledgeFileRelation with IDs {non_existing_or_deleted_ids} not found or already deleted.")

        relations_to_delete = [self.get_knowledge_file_relation_by_id(file_id) for file_id in
                               knowledge_file_relation_ids if file_id in existing_relations]
        for relation in relations_to_delete:
            relation.deleted = True  # 逻辑删除
            relation.update_time = datetime.now()  # 更新时间

        session.commit()
        return relations_to_delete
