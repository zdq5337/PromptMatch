'''
Description: 用户service
Author: Kyeoni hujr
Date: 2024-09-02 18:12:06
LastEditors: Kyeoni hujr
LastEditTime: 2024-09-11 10:40:55
'''
from typing import Annotated

from fastapi import Depends, status
from passlib.context import CryptContext
from sqlmodel import Session

from exception.api_exception import ApiException
from model.entity.user import User, Role
from model.request.user_request import UserCreateRequest
from model.vo.user_vo import UserRead
from repository.user_repository import UserRepository
from services.database.base import get_session
from services.user.jwt import generate_token
from utils.json_converter import JsonConverter
from utils.logger import logger

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, user_repo: Annotated[UserRepository, Depends(UserRepository)],
                 session: Annotated[Session, Depends(get_session)]) -> None:
        self.user_repo = user_repo
        self.session = session

    def create_user(self, user_create: UserCreateRequest) -> UserRead:
        """
        创建用户
        @param user_create: 用户创建信息
        @return: 用户信息
        """
        # 将验证后的数据转换为user模型
        user = User(**user_create.model_dump())
        logger.info(
            f"model-match services:user:UserService:create_user user: {JsonConverter.to_json(user)}")
        user_before = self.user_repo.get_user_by_username(user.username, self.session)
        if user_before:
            logger.info(
                f"model-match services:user:UserService:create_user user_before: {JsonConverter.to_json(user_before)}")
            raise ApiException(http_code=status.HTTP_400_BAD_REQUEST, message="客户信息已存在，请直接登录")
        user_all_count = self.user_repo.get_all_user_count(self.session)
        if user_all_count == 0:
            # 如果没有历史用户，则创建为管理员
            user.role = Role.ADMIN.value
        user.password = password_context.hash(user.password)
        user = self.user_repo.create_user(user, self.session)
        self.session.commit()
        self.session.refresh(user)
        return UserRead(**user.model_dump())

    def login_user(self, user_in: UserCreateRequest) -> UserRead:
        """
        用户登录

        @param user_in: 用户登录信息
        @return: 用户信息
        """
        # 校验客户名是否存在
        user = self.__check_if_user_exist(user_in.username)
        # 校验密码
        if not password_context.verify(user_in.password, user.password):
            raise ApiException(http_code=status.HTTP_400_BAD_REQUEST, message="用户名密码错误，请重新输入")
        else:
            # 生成token
            return UserRead(access_token=generate_token(user), token_type='bearer', **user.model_dump())

    def __check_if_user_exist(self, username: str):
        """
        检查用户是否存在

        @param username: 用户名
        @return: 用户是否存在
        """
        user = self.user_repo.get_user_by_username(username, self.session)
        logger.info(
            f"model-match services:user:UserService:user_login user_before: {JsonConverter.to_json(user)}")
        if not user:
            raise ApiException(http_code=status.HTTP_400_BAD_REQUEST, message="用户不存在，请先注册")
        else:
            return user
