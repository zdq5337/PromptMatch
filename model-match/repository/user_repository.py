'''
Description: 用户数据库
Author: Kyeoni hujr
Date: 2024-09-02 18:14:10
LastEditors: Kyeoni hujr
LastEditTime: 2024-09-06 16:50:14
'''
from sqlalchemy import func
from sqlmodel import Session, select
from sqlalchemy.engine import Result, ScalarResult
from model.entity.user import User


class UserRepository:
    def create_user(self, user: User, session: Session) -> User:
        '''
        创建一个新的用户

        :param user: 要创建的user对象
        :param session: SQLModel会话
        :return: 返回创建的user记录
        '''
        session.add(user)
        return user

    def get_user_by_username(self, username: str, session: Session) -> User:
        '''
        根据用户名获取用户信息

        :param username: 用户名
        :param session: SQLModel会话
        :return: 返回用户记录
        '''
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()

    def get_all_user_count(self, session: Session) -> int:
        """
        获取所有用户数量

        :param session: SQLModel会话
        :return: 返回用户数量
        """
        statement = select(func.count()).select_from(User)
        result: ScalarResult = session.exec(statement)
        result_all = result.all()
        return result_all[0]
