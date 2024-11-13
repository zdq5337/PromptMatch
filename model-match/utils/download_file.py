import os
from urllib.parse import urlparse

import requests

from utils.logger import logger


def extract_file_name(oss_url, local_filename=None) -> str:
    parsed_url = urlparse(oss_url)
    path = parsed_url.path
    file_name = local_filename or os.path.basename(path)
    file_name = file_name.split('?')[0]
    return file_name


def download_file_from_oss(oss_url, save_directory, local_filename=None) -> str:
    logger.info(
        f"model-match utils:download_file:download_file_from_oss oss_url: {oss_url}, save_directory: {save_directory}, local_filename: {local_filename}")
    # 从OSS URL中提取文件名称
    file_name = extract_file_name(oss_url, local_filename)

    # 构建保存的本地路径
    local_path = os.path.join(save_directory, file_name)

    # 发送HTTP请求下载文件
    response = requests.get(oss_url, stream=True)

    logger.info(f"model-match utils:download_file:download_file_from_oss response: {response}")
    # 检查请求是否成功
    if response.status_code == 200:
        # 获取文件大小
        file_size = int(response.headers.get('Content-Length', 0))
        logger.info(f"Downloading file from {oss_url}, size: {file_size} bytes")

        # 将文件内容写入本地文件
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        logger.info(f"File saved to {local_path}")
        return local_path
    else:
        logger.info(f"Failed to download file from {oss_url}")
        return None


if __name__ == "__main__":
    oss_url = "https://hq-prd-e-zine.oss-cn-szfinance-internal.aliyuncs.com/agent/prd/admin/hqins_model_match/product/8337de0b20174ed9bd1262f79b6a1be0.PDF"
    oss_url = "https://prompt-match.oss-cn-beijing.aliyuncs.com/knowledge/rag/%E6%A8%AA%E7%90%B4%E4%BA%BA%E5%AF%BF%E9%99%8D%E9%BE%99%E5%8D%81%E5%85%AB%E6%8E%8C.pdf?OSSAccessKeyId=LTAI5tCXUigrH9e2EBwRYbzE&Expires=1727781829&Signature=IZA1BTPbE5GbD5u%2B9r2ojqC6abQ%3D"
    local_path = "E:\File\\"

    # 调用函数下载文件
    download_success = download_file_from_oss(oss_url, local_path)
    logger.info(f"model-match utils:download_file:download_file_from_oss download_success: {download_success}")
    if download_success:
        print("Download completed successfully.")
    else:
        print("Download failed.")

# # 使用示例
# oss_url = "https://your_bucket_name.oss-cn-beijing.aliyuncs.com/your_file_path_in_oss"
# local_path = "/path/to/local/file"
#
# # 调用函数下载文件
# download_success = download_file_from_oss(oss_url, local_path)
# if download_success:
#     print("Download completed successfully.")
# else:
#     print("Download failed.")
