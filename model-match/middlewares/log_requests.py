from fastapi import Request

from utils.logger import logger

async def log_requests(request: Request, call_next):
    # 记录请求信息
    request_body = await request.body()
    try:
        decoded_body = request_body.decode('utf-8', errors='replace')
    except Exception as e:
        logger.error(f"Failed to decode request body: {e}")
        decoded_body = "<Failed to decode>"

    logger.info(f"Request URL: {request.url}, Request Method: {request.method}, Request Headers: {request.headers}, Request Body: {decoded_body}")

    # 继续处理请求
    response = await call_next(request)

    # 记录响应信息和内容
    logger.info(f"Response Status Code: {response.status_code}")

    return response
