import logging
import os
from typing import Annotated

from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.v1.application_api import router as application_router
from api.v1.application_chat_api import router as application_chat_router
from api.v1.chat_api import router as chat_router
from api.v1.file_api import router as file_router
from api.v1.knowledge_api import router as knowledge_router
from api.v1.knowledge_file_api import router as knowledge_file_router
from api.v1.large_model_api import router as large_model_router
from api.v1.login_api import router as login_router
from api.v1.prompt_chat_api import router as prompt_chat_router
from exception.api_exception import ApiException
from middlewares.log_requests import log_requests
from model.response_model import ResponseModel
from model.vo.user_vo import User
from setting import config
from utils.logger import configure
from utils.logger import logger
from utils.nacos_client import get_ip_address
from services.user.auth import get_current_active_user

# 配置 SQLModel 的日志级别为 DEBUG
logging.basicConfig()
logging.getLogger('sqlmodel.engine').setLevel(logging.DEBUG)

configure(log_level='DEBUG', log_file='./data/log/model-match.log')
app = FastAPI()
root_router = APIRouter()

root_router.include_router(knowledge_router, prefix="/v1", tags=["knowledge"])
root_router.include_router(knowledge_file_router, prefix="/v1", tags=["knowledge_file"])
root_router.include_router(large_model_router, prefix="/v1", tags=["large_model"])
root_router.include_router(application_router, prefix="/v1", tags=["application"])
root_router.include_router(chat_router, prefix="/v1", tags=["chat"])
root_router.include_router(application_chat_router, prefix="/v1", tags=["application_chat"])
root_router.include_router(prompt_chat_router, prefix="/v1", tags=["prompt_chat_router"])
root_router.include_router(login_router, prefix="/v1", tags=["login"])
root_router.include_router(file_router, prefix="/v1/file", tags=["file"])

# 定义应用程序信息
app_name = "model-mason"  # 应用程序名称
instance_ip = get_ip_address()  # 应用程序实例的IP地址
logger.info(f"model-match main.py instance_ip: {instance_ip}")

environ = os.environ


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    print(current_user.model_dump())
    return {"message": f"Hello {current_user.username}"}


# 定义异常处理器
@app.exception_handler(ApiException)
async def api_exception_handler(request, exc: ApiException):
    response = ResponseModel.fail(code=exc.get_code, message=exc.get_message)
    return JSONResponse(content=response.model_dump(), status_code=exc.get_http_code)


@app.exception_handler(Exception)
async def api_exception_handler(request, exc: Exception):
    response = ResponseModel.fail(code="999999", message="服务器内部错误")
    return JSONResponse(content=response.model_dump(), status_code=500)


# 将中间件应用于应用程序
app.middleware("http")(log_requests)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)

# 将根路由器挂载到应用上，设置根路径为 '/api'
app.include_router(root_router, prefix="/api/model-match")

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host='0.0.0.0', port=config['model-match']['port'], reload=True)
