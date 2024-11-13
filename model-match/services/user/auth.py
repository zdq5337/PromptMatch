'''
Description: 验证token有效性
Author: Kyeoni hujr
Date: 2024-09-10 09:09:38
LastEditors: Kyeoni hujr
LastEditTime: 2024-09-11 10:41:38
'''

from typing import Annotated

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from exception.api_exception import ApiException
from model.entity.user import User
from services.user.jwt import verify_token
from services.user.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_active_user(token: Annotated[str, Depends(oauth2_scheme)],
                            user_service: Annotated[UserService, Depends(UserService)]) -> User:
    credentials_exception = ApiException(
        http_code=status.HTTP_401_UNAUTHORIZED,
        message="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        success, user_data = verify_token(token)
        print(success, user_data)
        if success:
            username: str = user_data.get("username")
            if not username:
                raise credentials_exception
            token_data = User(**user_data)
            user = user_service.check_if_user_exist(token_data.username)
            if not user:
                raise credentials_exception
            return user
    except InvalidTokenError:
        raise credentials_exception
