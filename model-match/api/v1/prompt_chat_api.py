import logging
from threading import RLock

from fastapi import WebSocket, APIRouter, Depends, Query
from pyrate_limiter import Duration, Limiter, Rate

from services.knowledge.knowledge_service import KnowledgeService
from services.model_match.prompt_chat import prompt_model_match_templates_stream

router = APIRouter()

# 定义每分钟的最大请求数
max_requests_per_minute = 500

# 创建限流器
rate = Rate(max_requests_per_minute, Duration.MINUTE)
limiter = Limiter(rate)

# 创建一个锁来保证线程安全
lock = RLock()

# 配置日志记录
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)


@router.websocket("/prompt_chat")
async def chat_openai_prompt_templates_stream(
        websocket: WebSocket,
        model_name: str = Query(...),
        knowledge_id: int = Query(...),
        knowledgeService: KnowledgeService = Depends(KnowledgeService)
):
    try:
        # 尝试获取限流令牌
        limiter.try_acquire("prompt_chat_limit")
        logger.info(f"model-match: api v1 prompt_chat_api: chat_openai_prompt_templates_stream: model_name: {model_name}, knowledge_id: {knowledge_id}")
        # 处理请求
        return await prompt_model_match_templates_stream(
            websocket=websocket,
            model_name=model_name,
            knowledge_id=knowledge_id,
            knowledgeService=knowledgeService
        )
    except Exception as e:
        # 打印异常信息，了解请求为何被拒绝
        logger.error(
            f"model-match: api v1 prompt_chat_api: chat_openai_prompt_templates_stream error: {e}"
        )
        await websocket.close(code=1008, reason=str(e))
