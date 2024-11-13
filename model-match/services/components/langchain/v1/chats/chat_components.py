from langchain_community.chat_models.baidu_qianfan_endpoint import QianfanChatEndpoint
from langchain_community.chat_models.openai import ChatOpenAI
from langchain_core.language_models import BaseChatModel

from constants.large_model_enum import LargeModelName, LargeModelVendor
from services.rate_limiter.siliconflow_rate_limiter import SiliconFlowRateLimiter
from setting import config
from utils.generate_token import generate_zhipu_token


def get_baidu_chat(large_model: LargeModelName) -> BaseChatModel:
    """
    构建百度大模型
    :param large_model: 模型名称
    :return:  BaseChatModel
    """
    return QianfanChatEndpoint(qianfan_ak=config['large-model']['qianfan-ak'],
                               qianfan_sk=config['large-model']['qianfan-sk'],
                               temperature=0.01,
                               model=large_model.vendor_name,
                               streaming=True, )


def get_zhipu_chat(large_model: LargeModelName) -> BaseChatModel:
    """
    构建智谱大模型

    :param large_model: 模型名称
    :return:  BaseChatModel
    """
    key = generate_zhipu_token(config['large-model']['glm-key'], 3600)
    return ChatOpenAI(temperature=0.01,
                      openai_api_key=key,
                      model_name=large_model.vendor_name,
                      openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
                      streaming=True, )


def get_kimi_chat(large_model: LargeModelName) -> BaseChatModel:
    """
    构建Kimi大模型
    :param large_model: 模型名称
    :return:  BaseChatModel
    """
    return ChatOpenAI(openai_api_key=config['large-model']['kimi-key'],
                      openai_api_base="https://api.moonshot.cn/v1",
                      model_name=large_model.vendor_name,
                      temperature=0.01,
                      streaming=True,
                      )


# Split the siliconflow-key string into a list of keys
api_keys = config['large-model']['siliconflow-key'].split(',')

# Instantiate a rate limiter for each API key
rate_limiters = [SiliconFlowRateLimiter(max_requests_per_minute=60, max_tokens_per_minute=1000) for _ in api_keys]

current_key_index = 0


def get_siliconflow_chat(large_model: LargeModelName) -> tuple[BaseChatModel, SiliconFlowRateLimiter]:
    """
    构建SiliconFlow大模型
    :param large_model: 模型名称
    :return:  BaseChatModel, RateLimiter3
    """
    global current_key_index

    # 确保 current_key_index 在有效范围内
    if current_key_index >= len(api_keys):
        current_key_index = 0

    # 轮换 API 密钥和对应的速率限制器
    api_key = api_keys[current_key_index]
    rate_limiter = rate_limiters[current_key_index]
    current_key_index = (current_key_index + 1) % len(api_keys)

    return ChatOpenAI(openai_api_key=api_key,
                      openai_api_base="https://api.siliconflow.cn/v1",
                      model_name=large_model.vendor_name,
                      temperature=0.01,
                      streaming=True), rate_limiter


async def get_chat_model(chat: BaseChatModel, large_model: LargeModelName) -> tuple[BaseChatModel, SiliconFlowRateLimiter]:
    """
    获取对应的聊天模型
    :param chat:  聊天模型
    :param large_model:  大模型数据信息
    :return:  聊天模型, RateLimiter3
    """
    rate_limiter = None
    if large_model.model_vendor == LargeModelVendor.BAIDU.vendor_name:
        chat = get_baidu_chat(large_model)
    if large_model.model_vendor == LargeModelVendor.ZHIPU.vendor_name:
        chat = get_zhipu_chat(large_model)
    if large_model.model_vendor == LargeModelVendor.KIMI.vendor_name:
        chat = get_kimi_chat(large_model)
    if large_model.model_vendor == LargeModelVendor.SILICON_FLOW.vendor_name:
        chat, rate_limiter = get_siliconflow_chat(large_model)
    return chat, rate_limiter
