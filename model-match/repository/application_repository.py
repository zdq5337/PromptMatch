from datetime import datetime
from typing import List, Optional

from sqlmodel import Session

from model.entity.application import Application


class ApplicationRepository:
    def get_application_by_id(self, application_id: int, session: Session) -> Optional[Application]:
        """
        根据ID获取Application记录。

        :param application_id: 要获取的Application记录的ID
        :param session: SQLModel会话
        :return: 返回获取到的Application记录，如果记录不存在则返回None
        """
        return session.query(Application).filter(Application.id == application_id, Application.deleted.is_(False)).first()

    def get_all_applications(self, session: Session) -> List[Application]:
        """
        获取所有未删除的Application记录。

        :param session: SQLModel会话
        :return: 返回所有未删除的Application记录的列表
        """
        return session.query(Application).filter(Application.deleted.is_(False)).all()

    def create_application(self, application: Application, session: Session) -> Application:
        """
        创建一个新的Application记录。

        :param application: 要创建的Application对象
        :param session: SQLModel会话
        :return: 返回创建的Application记录
        """
        session.add(application)
        return application

    def update_application(self, old_application: Application, new_application: Application,
                           session: Session) -> Application:
        """
        更新给定的Application记录。

        :param old_application: 要更新的Application对象
        :param new_application: 包含更新数据的新Application对象
        :param session: SQLModel会话
        :return: 返回更新后的Application记录
        """
        for key, value in new_application.model_dump().items():
            setattr(old_application, key, value)
        return old_application

    def delete_application(self, application: Application, session: Session) -> Application:
        """
        逻辑删除给定的Application记录。

        :param application: 要逻辑删除的Application对象
        :param session: SQLModel会话
        :return: 返回逻辑删除后的Application记录
        """
        application.deleted = True  # 逻辑删除
        application.update_time = datetime.now()  # 更新时间
        return application
