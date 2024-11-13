'''
Description: 登录接口
Author: Kyeoni hujr
Date: 2024-09-02 16:00:23
LastEditors: Kyeoni hujr
LastEditTime: 2024-09-04 18:13:33
'''
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from model.request.user_request import UserCreateRequest
from model.response_model import ResponseModel
from services.user.user_service import UserService

router = APIRouter()


# 注册接口
@router.post("/users", response_model=ResponseModel, status_code=HTTPStatus.CREATED)
def create_user(user_create_request: UserCreateRequest, service: Annotated[UserService, Depends(UserService)]):
    return ResponseModel.ok(service.create_user(user_create_request))


# 登录接口
@router.post("/users/login", response_model=ResponseModel, status_code=HTTPStatus.OK)
def login_user(user_create_request: UserCreateRequest, service: Annotated[UserService, Depends(UserService)]):
    return ResponseModel.ok(service.login_user(user_create_request))
