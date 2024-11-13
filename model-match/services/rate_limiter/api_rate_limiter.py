from pyrate_limiter import Duration, Limiter, Rate
import time

# 定义每分钟的最大请求数
max_requests_per_minute = 800

# 创建限流器
rate = Rate(max_requests_per_minute, Duration.MINUTE)
limiter = Limiter(rate)

def handle_request():
    try:
        limiter.try_acquire("application_chat_limit")
        # 处理请求
        print("请求被允许")
    except Exception as e:
        # 打印异常信息，了解请求为何被拒绝
        print(f"请求超出限制: {e}")

# 测试限流功能
if __name__ == "__main__":
    for _ in range(1000):
        handle_request()
        # 模拟更真实的请求间隔
        time.sleep(0.001)  # 调整为更短的间隔，或者使用随机间隔