from datetime import datetime
from typing import List

from sqlmodel import Session

from model.entity.knowledge import Knowledge


class KnowledgeRepository:
    def get_knowledge_by_id(self, knowledge_id: int, session: Session) -> Knowledge:
        """
        根据ID获取Knowledge记录。

        :param knowledge_id: 要获取的Knowledge记录的ID
        :param session: SQLModel会话
        :return: 返回获取到的Knowledge记录，如果记录不存在则返回None
        """
        return session.query(Knowledge).filter(Knowledge.id == knowledge_id, Knowledge.deleted.is_(False)).first()

    def get_all_knowledge(self, session: Session) -> List[Knowledge]:
        """
        获取所有未删除的Knowledge记录。

        :param session: SQLModel会话
        :return: 返回所有未删除的Knowledge记录的列表
        """
        return session.query(Knowledge).filter(Knowledge.deleted.is_(False)).all()

    def create_knowledge(self, knowledge: Knowledge, session: Session) -> Knowledge:
        """
        创建一个新的Knowledge记录。

        :param knowledge: 要创建的Knowledge对象
        :param session: SQLModel会话
        :return: 返回创建的Knowledge记录
        """
        session.add(knowledge)
        return knowledge

    def update_knowledge(self, new_knowledge: Knowledge, old_knowledge: Knowledge, session: Session) -> Knowledge:
        """
        更新给定的Knowledge记录。

        :param new_knowledge: 包含更新数据的新Knowledge对象
        :param old_knowledge: 要更新的Knowledge对象
        :param session: SQLModel会话
        :return: 返回更新后的Knowledge记录
        """
        allowed_keys = ['name', 'description', 'icon', 'modifier', 'modifier_id', 'update_time']
        for key, value in new_knowledge.model_dump().items():
            if key in allowed_keys:
                setattr(old_knowledge, key, value)
        return old_knowledge

    def delete_knowledge(self, knowledge: Knowledge, session: Session) -> Knowledge:
        """
        逻辑删除给定的Knowledge记录。

        :param knowledge: 要逻辑删除的Knowledge对象
        :param session: SQLModel会话
        :return: 返回逻辑删除后的Knowledge记录
        """
        knowledge.deleted = True  # 逻辑删除
        knowledge.update_time = datetime.now()  # 更新时间
        return knowledge
