import argparse

import yaml

from utils.logger import logger


def load_config(environment):
    with open('config.yaml', 'r', encoding='utf-8') as stream:
        config = yaml.safe_load(stream)
        return config.get(environment, {})


# 创建参数解析器
parser = argparse.ArgumentParser()
parser.add_argument('--environment', default='dat', help='Environment to use')
args = parser.parse_args()

# 选择特定环境的配置
environment = args.environment  # 可以根据需要修改环境
logger.info(f"Loading config: {environment}")
config = load_config(environment)
