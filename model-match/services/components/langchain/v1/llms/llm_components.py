from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint
from langchain_community.llms.openai import OpenAI
from langchain_core.language_models import BaseLLM

from constants.large_model_enum import LargeModelVendor, LargeModelName
from setting import config
from utils.generate_token import generate_zhipu_token


def get_baidu_llm(large_model) -> BaseLLM:
    """
    构建百度大模型
    :param large_model: 模型名称
    :return:  BaseLLM
    """
    return QianfanLLMEndpoint(temperature=0.01,
                              qianfan_ak=config['large-model']['qianfan-ak'],
                              qianfan_sk=config['large-model']['qianfan-sk'],
                              streaming=True,
                              model=large_model.vendor_name, )


def get_zhipu_llm(large_model) -> BaseLLM:
    """
    构建智谱大模型

    :param large_model: 模型名称
    :return:  BaseLLM
    """
    key = generate_zhipu_token(config['large-model']['glm-key'], 3600)
    return OpenAI(temperature=0.01,
                  openai_api_key=key,
                  model=large_model.vendor_name,
                  streaming=True,
                  openai_api_base="https://open.bigmodel.cn/api/paas/v4/chat",
                  )


def get_kimi_llm(large_model) -> BaseLLM:
    """
    构建Kimi大模型
    :param large_model: 模型名称
    :return:  BaseLLM
    """
    return OpenAI(
        temperature=0.01,
        openai_api_key=config['large-model']['kimi-key'],
        openai_api_base="https://api.moonshot.cn/v1/chat",
        model_name=large_model.vendor_name,
        streaming=True,
    )


async def get_llm_model(large_model: LargeModelName, llm: BaseLLM) -> BaseLLM:
    # ... get_llm_model的实现 ...
    if large_model.model_vendor == LargeModelVendor.BAIDU.vendor_name:
        llm = get_baidu_llm(large_model)
    if large_model.model_vendor == LargeModelVendor.ZHIPU.vendor_name:
        llm = get_zhipu_llm(large_model)
    if large_model.model_vendor == LargeModelVendor.KIMI.vendor_name:
        llm = get_kimi_llm(large_model)
    return llm
