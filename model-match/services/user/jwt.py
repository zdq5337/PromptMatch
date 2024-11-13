'''
Description: jwt相关
Author: Kyeoni hujr
Date: 2024-09-09 16:04:44
LastEditors: Kyeoni hujr
LastEditTime: 2024-09-09 18:35:32
'''
from datetime import datetime

import jwt
from jwt.exceptions import InvalidTokenError

from model.vo.user_vo import User

ALGORITHM = 'HS256'
SECRET_KEY = "4c518415b573a63692a44a178dc134c04d7574cab71bcf7589dfa644c217b511"


def generate_token(user: User) -> str:
    payload = {
        **user.model_dump(exclude={'password', 'create_time', 'last_login_time'}),
        'exp': int(datetime.now().timestamp()) + 60 * 60 * 24 * 7
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True, payload
    except InvalidTokenError:
        return False, None
