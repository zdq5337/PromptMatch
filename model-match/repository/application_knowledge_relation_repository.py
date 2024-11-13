from datetime import datetime
from typing import Optional, List

from sqlmodel import Session

from model.entity.application_knowledge_relation import ApplicationKnowledgeRelation


class ApplicationKnowledgeRelationRepository:

    def get_application_knowledge_relation_by_id(self, relation_id: int, session: Session) -> Optional[
        ApplicationKnowledgeRelation]:
        """
        根据ID获取ApplicationKnowledgeRelation记录。
        :param relation_id:  要获取的ApplicationKnowledgeRelation记录的ID
        :param session:  SQLModel会话
        :return:  返回获取到的ApplicationKnowledgeRelation记录
        """
        return session.query(ApplicationKnowledgeRelation).filter(ApplicationKnowledgeRelation.id == relation_id,
                                                                  ApplicationKnowledgeRelation.deleted == False).first()

    def get_application_knowledge_relation_by_application_id(self, application_id: int, session: Session) -> List[
        ApplicationKnowledgeRelation]:
        """
        根据application_id获取ApplicationKnowledgeRelation记录。
        :param application_id:  要获取的ApplicationKnowledgeRelation记录的application_id
        :param session:  SQLModel会话
        :return:    返回获取到的ApplicationKnowledgeRelation记录
        """
        return session.query(ApplicationKnowledgeRelation).filter(
            ApplicationKnowledgeRelation.application_id == application_id,
            ApplicationKnowledgeRelation.deleted == False).all()

    def get_all_application_knowledge_relations(self, session: Session) -> List[ApplicationKnowledgeRelation]:
        """
        获取所有的ApplicationKnowledgeRelation记录。
        :param session:  SQLModel会话
        :return:  返回所有的ApplicationKnowledgeRelation记录
        """
        return session.query(ApplicationKnowledgeRelation).filter(ApplicationKnowledgeRelation.deleted == False).all()

    def create_application_knowledge_relation(self, relation: ApplicationKnowledgeRelation,
                                              session: Session) -> ApplicationKnowledgeRelation:
        """
        创建一个新的ApplicationKnowledgeRelation记录。
        :param relation:  要创建的ApplicationKnowledgeRelation记录
        :param session:  SQLModel会话
        :return:  返回创建的ApplicationKnowledgeRelation记录
        """
        session.add(relation)
        return relation

    def update_application_knowledge_relation(self, old_relation: ApplicationKnowledgeRelation,
                                              new_relation: ApplicationKnowledgeRelation,
                                              session: Session) -> ApplicationKnowledgeRelation:
        """
        更新给定的ApplicationKnowledgeRelation记录。
        :param old_relation:  要更新的ApplicationKnowledgeRelation记录
        :param new_relation:  新的ApplicationKnowledgeRelation记录
        :param session:  SQLModel会话
        :return:  返回更新后的ApplicationKnowledgeRelation记录
        """
        for key, value in new_relation.model_dump().items():
            setattr(old_relation, key, value)
        return old_relation

    def delete_application_knowledge_relation(self, application_knowledge_relation: ApplicationKnowledgeRelation,
                                              session: Session) -> ApplicationKnowledgeRelation:
        """
        删除给定的ApplicationKnowledgeRelation记录。
        :param application_knowledge_relation:  要删除的ApplicationKnowledgeRelation记录
        :param session:  SQLModel会话
        :return:  返回删除后的ApplicationKnowledgeRelation记录
        """
        application_knowledge_relation.deleted = True  # 逻辑删除
        application_knowledge_relation.update_time = datetime.now()  # 更新时间
        return application_knowledge_relation

    def delete_by_application_id(self, application_id: int, session: Session):
        """
        根据application_id删除ApplicationKnowledgeRelation记录。
        :param application_id:  要删除的ApplicationKnowledgeRelation记录的application_id
        :param session:  SQLModel会话
        :return:  无返回值
        """

        # 查询application_id对应的所有ApplicationKnowledgeRelation记录
        relations_to_delete = session.query(ApplicationKnowledgeRelation).filter(
            ApplicationKnowledgeRelation.application_id == application_id,
            ApplicationKnowledgeRelation.deleted == False
        ).all()

        # 遍历查询结果，设置deleted字段为True，并更新update_time字段
        for relation in relations_to_delete:
            relation.deleted = True
            relation.update_time = datetime.now()

        # 此处不需要session.add()，因为 relations_to_delete 中的对象已经是会话的一部分
        # 当你提交会话时，所有的改动都会被保存到数据库
