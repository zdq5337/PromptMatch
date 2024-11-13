# -*- coding: utf-8 -*-
import os
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from typing import Optional

from setting import config
from utils.logger import logger


# 定义常量
ACCESS_KEY_ID = config['aliyun']['oss']['access-key-id']
ACCESS_KEY_SECRET = config['aliyun']['oss']['access-key-secret']
OSS_URL = config['aliyun']['oss']['url']
BUCKET_NAME = config['aliyun']['oss']['bucket-name']

# 设置环境变量
os.environ['OSS_ACCESS_KEY_ID'] = ACCESS_KEY_ID
os.environ['OSS_ACCESS_KEY_SECRET'] = ACCESS_KEY_SECRET

# 从环境变量中获取访问凭证
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())

# 创建Bucket对象
bucket = oss2.Bucket(auth, OSS_URL, BUCKET_NAME)


def upload_file_to_oss(file_data: bytes, oss_target_path: str) -> Optional[str]:
    # 上传文件
    result = bucket.put_object(oss_target_path, file_data)
    logger.info(f'model-match/utils/aliyun_oss.py upload_file_to_oss: Upload result: {result} {result.request_id}')

    # 检查上传结果
    if result.status == 200:
        logger.info(f'model-match/utils/aliyun_oss.py upload_file_to_oss: File uploaded successfully to {oss_target_path}')
        return oss_target_path
    else:
        logger.error(f'model-match/utils/aliyun_oss.py upload_file_to_oss: Error uploading file to {oss_target_path}')
        return None


def get_oss_file_url(oss_target_path: str) -> Optional[str]:
    try:
        # 生成下载文件的签名URL，有效时间为3600秒。
        # 设置slash_safe为True，OSS不会对Object完整路径中的正斜线（/）进行转义，此时生成的签名URL可以直接使用。
        url = bucket.sign_url('GET', oss_target_path, 3600, slash_safe=True)
        logger.info(f"model-match/utils/aliyun_oss.py get_oss_file_url: File URL: {url}")
        return url
    except Exception as e:
        logger.error(f"model-match/utils/aliyun_oss.py get_oss_file_url: Error: {str(e)}")
        return None

# 用法示例
if __name__ == "__main__":
    # file_path = r"D:\BaiduNetdiskDownload\二、框架源码专题\01-Spring底层核心原理解析-周瑜\01-Spring底层核心原理解析 ​1.pdf"
    #
    # # 读取文件内容
    # with open(file_path, 'rb') as file:
    #     file_data = file.read()
    #
    # oss_target_path = "111/exampleobject.pdf"
    #
    # upload_success = upload_file_to_oss(file_data, oss_target_path)
    # if upload_success:
    #     print("Upload completed successfully.")
    # else:
    #     print("Upload failed.")

    print(get_oss_file_url("111/exampleobject.pdf"))