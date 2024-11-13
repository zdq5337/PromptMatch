import logging
from threading import RLock

from fastapi import WebSocket, APIRouter, Query, Depends
from pyrate_limiter import Duration, Limiter, Rate

from services.application.application_chat import application_chat_history_continuous_stream
from services.application.application_service import ApplicationService
from services.knowledge.knowledge_service import KnowledgeService

router = APIRouter()

# 定义每分钟的最大请求数
max_requests_per_minute = 200

# 创建限流器
rate = Rate(max_requests_per_minute, Duration.MINUTE)
limiter = Limiter(rate)

# 创建一个锁来保证线程安全
lock = RLock()

# 配置日志记录
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)


@router.websocket("/application_chat")
async def chat_openai_prompt_templates_history_continuous_stream(
        websocket: WebSocket,
        application_id: int = Query(...),
        applicationService: ApplicationService = Depends(ApplicationService),
        knowledgeService: KnowledgeService = Depends(KnowledgeService)
):
    try:
        # 尝试获取限流令牌
        await limiter.try_acquire("application_chat_limit")
        # 处理请求
        return await application_chat_history_continuous_stream(
            websocket=websocket,
            application_id=application_id,
            applicationService=applicationService,
            knowledgeService=knowledgeService
        )
    except Exception as e:
        # 打印异常信息，了解请求为何被拒绝
        logger.error(
            f"model-match: api v1 application_chat_api: chat_openai_prompt_templates_history_continuous_stream error: {e}")
        await websocket.close(code=1008, reason=str(e))
