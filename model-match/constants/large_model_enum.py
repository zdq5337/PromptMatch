from enum import Enum
from typing import Any

from utils.logger import logger


class LargeModelVendor(Enum):
    BAIDU = (1, "百度", "百度智能云千帆大模型平台提供先进的生成式AI生产及应用全流程开发工具链，"
                        "同时文心一言赋能百度智能云产品全面升级，企业可根据需求，"
                        "选取相应的云服务和产品，方便、快捷、低成本地构建自己的模型和应用")
    ZHIPU = (2, "智谱", "智谱AI是由清华大学计算机系技术成果转化而来的公司，致力于打造新一代认知智能通用模型。")
    KIMI = (
    3, "月之暗面", "月之暗面(Moonshot AI) 创立于2023年3月，致力于寻求将能源转化为智能的最优解，通过产品与用户共创智能")
    SILICON_FLOW = (4, "硅基流动", "SiliconCloud，高性价比的GenAI云服务")

    def __init__(self, serial_number, vendor_name, description):
        self.serial_number = serial_number
        self.vendor_name = vendor_name
        self.description = description


class SiliconFlowModelName(Enum):
    QWEN_2_5_7B_INSTRUCT = (1, "Qwen/Qwen2.5-7B-Instruct", LargeModelVendor.SILICON_FLOW.vendor_name)
    QWEN_2_7B_INSTRUCT = (2, "Qwen/Qwen2-7B-Instruct", LargeModelVendor.SILICON_FLOW.vendor_name)
    QWEN_2_1_5B_CHAT = (3, "Qwen/Qwen2-1.5B-Chat", LargeModelVendor.SILICON_FLOW.vendor_name)
    GLM_4_9B_CHAT = (4, "THUDM/glm-4-9b-chat", LargeModelVendor.SILICON_FLOW.vendor_name)
    CHATGLM3_6B = (5, "THUDM/chatglm3-6b", LargeModelVendor.SILICON_FLOW.vendor_name)
    YI_1_5_9B_CHAT_16K = (6, "01-ai/Yi-1.5-9B-Chat-16K", LargeModelVendor.SILICON_FLOW.vendor_name)
    YI_1_5_6B_CHAT = (7, "01-ai/Yi-1.5-6B-Chat", LargeModelVendor.SILICON_FLOW.vendor_name)
    GEMMA_2_9B_IT = (8, "google/gemma-2-9b-it", LargeModelVendor.SILICON_FLOW.vendor_name)
    INTERNLM2_5_7B_CHAT = (9, "internlm/internlm2_5-7b-chat", LargeModelVendor.SILICON_FLOW.vendor_name)
    META_LLAMA_3_8B_INSTRUCT = (10, "meta-llama/Meta-Llama-3-8B-Instruct", LargeModelVendor.SILICON_FLOW.vendor_name)
    META_LLAMA_3_1_8B_INSTRUCT = (
    11, "meta-llama/Meta-Llama-3.1-8B-Instruct", LargeModelVendor.SILICON_FLOW.vendor_name)
    MISTRAL_7B_INSTRUCT_V0_2 = (12, "mistralai/Mistral-7B-Instruct-v0.2", LargeModelVendor.SILICON_FLOW.vendor_name)

    # QWEN_2_5_CODER_7B_INSTRUCT = (13, "Qwen/Qwen2.5-Coder-7B-Instruct", LargeModelVendor.SILICON_FLOW.vendor_name)
    # QWEN_2_72B_INSTRUCT = (14, "Vendor-A/Qwen/Qwen2-72B-Instruct", LargeModelVendor.SILICON_FLOW.vendor_name)

    def __init__(self, model_number, model_name, model_vendor):
        self.serial_number = model_number
        self.vendor_name = model_name
        self.model_vendor = model_vendor


class LargeModelName(Enum):
    QWEN_2_5_7B_INSTRUCT = (1, "Qwen/Qwen2.5-7B-Instruct", LargeModelVendor.SILICON_FLOW.vendor_name)
    QWEN_2_7B_INSTRUCT = (2, "Qwen/Qwen2-7B-Instruct", LargeModelVendor.SILICON_FLOW.vendor_name)
    QWEN_2_1_5B_CHAT = (3, "Qwen/Qwen2-1.5B-Chat", LargeModelVendor.SILICON_FLOW.vendor_name)
    GLM_4_9B_CHAT = (4, "THUDM/glm-4-9b-chat", LargeModelVendor.SILICON_FLOW.vendor_name)
    CHATGLM3_6B = (5, "THUDM/chatglm3-6b", LargeModelVendor.SILICON_FLOW.vendor_name)
    YI_1_5_9B_CHAT_16K = (6, "01-ai/Yi-1.5-9B-Chat-16K", LargeModelVendor.SILICON_FLOW.vendor_name)
    YI_1_5_6B_CHAT = (7, "01-ai/Yi-1.5-6B-Chat", LargeModelVendor.SILICON_FLOW.vendor_name)
    GEMMA_2_9B_IT = (8, "google/gemma-2-9b-it", LargeModelVendor.SILICON_FLOW.vendor_name)
    INTERNLM2_5_7B_CHAT = (9, "internlm/internlm2_5-7b-chat", LargeModelVendor.SILICON_FLOW.vendor_name)
    META_LLAMA_3_8B_INSTRUCT = (10, "meta-llama/Meta-Llama-3-8B-Instruct", LargeModelVendor.SILICON_FLOW.vendor_name)
    META_LLAMA_3_1_8B_INSTRUCT = (
        11, "meta-llama/Meta-Llama-3.1-8B-Instruct", LargeModelVendor.SILICON_FLOW.vendor_name)
    MISTRAL_7B_INSTRUCT_V0_2 = (12, "mistralai/Mistral-7B-Instruct-v0.2", LargeModelVendor.SILICON_FLOW.vendor_name)

    def __init__(self, model_number, model_name, model_vendor):
        self.serial_number = model_number
        self.vendor_name = model_name
        self.model_vendor = model_vendor


def get_all_model_name() -> list[dict[str, Any]]:
    """
    获取所有模型名称
    :return:  返回所有模型名称的 JSON 格式字符串
    """
    model_names = []
    for model in SiliconFlowModelName:
        model_info = {
            "serial_number": model.serial_number,
            "vendor_name": model.vendor_name,
            "model_vendor": model.model_vendor
        }
        logger.info(f"model_info: {model_info}")
        model_names.append(model_info)
    logger.info(f"model_names: {model_names}")
    # return json.dumps(model_names, ensure_ascii=False)
    return model_names
