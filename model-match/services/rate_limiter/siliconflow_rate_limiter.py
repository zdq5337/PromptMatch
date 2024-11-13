import time
from collections import deque, defaultdict

from langchain_openai import ChatOpenAI

from services.components.langchain.v1.prompts.generate_prompts import generation_prompt_template

class SiliconFlowRateLimiter:
    """
    限速规则
    https://docs.siliconflow.cn/docs/rate-limits-rules
    """

    def __init__(self, max_requests_per_minute, max_tokens_per_minute):
        self.max_requests_per_minute = max_requests_per_minute
        self.max_tokens_per_minute = max_tokens_per_minute
        self.request_times = defaultdict(deque)
        self.token_count = defaultdict(int)

    def _wait_if_needed(self, model_name):
        current_time = time.time()
        window_start = current_time - 60

        # 移除窗口外的请求时间戳
        while self.request_times[model_name] and self.request_times[model_name][0] < window_start:
            self.request_times[model_name].popleft()

        # 计算当前窗口内的请求数和令牌数
        current_requests = len(self.request_times[model_name])
        current_tokens = self.token_count[model_name]

        # 如果超过限制，等待直到可以处理新的请求
        while current_requests >= self.max_requests_per_minute or current_tokens >= self.max_tokens_per_minute:
            time.sleep(1)
            current_time = time.time()
            window_start = current_time - 60

            # 移除窗口外的请求时间戳
            while self.request_times[model_name] and self.request_times[model_name][0] < window_start:
                self.request_times[model_name].popleft()

            current_requests = len(self.request_times[model_name])
            current_tokens = self.token_count[model_name]

    def add_request(self, model_name, token_count):
        self._wait_if_needed(model_name)
        self.request_times[model_name].append(time.time())
        self.token_count[model_name] += token_count


class RateLimiterForKey:
    """
    限速规则
    https://docs.siliconflow.cn/docs/rate-limits-rules
    """

    def __init__(self, max_requests_per_minute, max_tokens_per_minute, num_keys=2):
        self.max_requests_per_minute = max_requests_per_minute
        self.max_tokens_per_minute = max_tokens_per_minute
        self.num_keys = num_keys
        self.request_times = [defaultdict(deque) for _ in range(num_keys)]
        self.token_count = [defaultdict(int) for _ in range(num_keys)]
        self.current_key = 0

    def _wait_if_needed(self, key):
        current_time = time.time()
        window_start = current_time - 60

        # 移除窗口外的请求时间戳
        while self.request_times[key][key] and self.request_times[key][key][0] < window_start:
            self.request_times[key][key].popleft()

        # 计算当前窗口内的请求数和令牌数
        current_requests = len(self.request_times[key][key])
        current_tokens = self.token_count[key][key]

        # 如果超过限制，等待直到可以处理新的请求
        while current_requests >= self.max_requests_per_minute or current_tokens >= self.max_tokens_per_minute:
            time.sleep(1)
            current_time = time.time()
            window_start = current_time - 60

            # 移除窗口外的请求时间戳
            while self.request_times[key][key] and self.request_times[key][key][0] < window_start:
                self.request_times[key][key].popleft()

            current_requests = len(self.request_times[key][key])
            current_tokens = self.token_count[key][key]

    def add_request(self, model_name, token_count):
        key = self.current_key
        self._wait_if_needed(key)
        self.request_times[key][model_name].append(time.time())
        self.token_count[key][model_name] += token_count

        # 切换到下一个 key
        self.current_key = (self.current_key + 1) % self.num_keys
