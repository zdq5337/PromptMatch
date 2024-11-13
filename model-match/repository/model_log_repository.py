from datetime import datetime
from typing import Optional, List

from sqlmodel import Session, select

from model.entity.model_log import ModelLog  # 假设ModelLog实体已经定义

class ModelLogRepository:
    def get_model_log_by_id(self, log_id: int, session: Session) -> Optional[ModelLog]:
        """
        根据ID获取ModelLog记录。

        :param log_id: 要获取的ModelLog记录的ID
        :param session: SQLModel会话
        :return: 返回获取到的ModelLog记录，如果记录不存在则返回None
        """
        statement = select(ModelLog).where(ModelLog.id == log_id)
        result = session.exec(statement)
        return result.first()

    def get_model_log_by_model_name(self, model_name: str, session: Session) -> List[ModelLog]:
        """
        根据model_name获取ModelLog记录。

        :param model_name: 要获取的ModelLog记录的model_name
        :param session: SQLModel会话
        :return: 返回获取到的ModelLog记录列表
        """
        statement = select(ModelLog).where(ModelLog.model_name == model_name)
        result = session.exec(statement)
        return result.all()

    def get_all_model_logs(self, session: Session) -> List[ModelLog]:
        """
        获取所有ModelLog记录。

        :param session: SQLModel会话
        :return: 返回所有ModelLog记录的列表
        """
        statement = select(ModelLog)
        result = session.exec(statement)
        return result.all()

    def create_model_log(self, log: ModelLog, session: Session) -> ModelLog:
        """
        创建一个新的ModelLog记录。

        :param log: 要创建的ModelLog记录
        :param session: SQLModel会话
        :return: 返回创建的ModelLog记录
        """
        session.add(log)
        session.commit()
        session.refresh(log)
        return log

    def update_model_log(self, old_log: ModelLog, new_log: ModelLog, session: Session) -> ModelLog:
        """
        更新给定的ModelLog记录。

        :param old_log: 要更新的ModelLog记录
        :param new_log: 新的ModelLog记录
        :param session: SQLModel会话
        :return: 返回更新后的ModelLog记录
        """
        allowed_keys = ['model_name', 'model_source', 'question', 'answer', 'document', 'update_time']
        for key, value in new_log.model_dump().items():
            if key in allowed_keys:
                setattr(old_log, key, value)
        session.add(old_log)
        session.commit()
        session.refresh(old_log)
        return old_log

    def delete_model_log(self, model_log: ModelLog, session: Session) -> ModelLog:
        """
        删除给定的ModelLog记录。

        :param model_log: 要删除的ModelLog记录
        :param session: SQLModel会话
        :return: 返回删除后的ModelLog记录
        """
        model_log.deleted = True  # 逻辑删除
        model_log.update_time = datetime.now()  # 更新时间
        session.add(model_log)
        session.commit()
        session.refresh(model_log)
        return model_log

    def delete_by_model_name(self, model_name: str, session: Session):
        """
        根据model_name删除ModelLog记录。

        :param model_name: 要删除的ModelLog记录的model_name
        :param session: SQLModel会话
        :return: 无返回值
        """
        logs_to_delete = session.exec(select(ModelLog).where(ModelLog.model_name == model_name)).all()

        for log in logs_to_delete:
            log.deleted = True
            log.update_time = datetime.now()
        session.commit()
