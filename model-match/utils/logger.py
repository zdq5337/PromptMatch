from pathlib import Path
from typing import Optional

import orjson
from loguru import logger
from rich.logging import RichHandler
import logging
from rich.console import Console

VALID_LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


# 设置 SQLAlchemy 的日志级别为 DEBUG
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


def serialize(record):
    subset = {
        'timestamp': record['time'].timestamp(),
        'message': record['message'],
        'level': record['level'].name,
        'module': record['module'],
    }
    return orjson.dumps(subset)


def patching(record):
    record['extra']['serialized'] = serialize(record)


def configure(log_level: Optional[str] = None, log_file: Optional[Path] = None):
    if log_level is None:
        log_level = 'INFO'
    # Human-readable
    log_format = '<level>[{thread.name} {name}:{line}]</level> - <level>{message}</level>'

    # log_format = log_format_dev if log_level.upper() == "DEBUG" else log_format_prod
    logger.remove()  # Remove default handlers
    logger.patch(patching)
    # Configure loguru to use RichHandler
    logger.configure(handlers=[{
        'sink': RichHandler(rich_tracebacks=True, markup=True),
        'format': log_format,
        'level': log_level.upper(),
    }])

    if not log_file:
        log_file = 'data/model-match.log'

    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger.add(
        sink=str(log_file),
        level=log_level.upper(),
        format=log_format,
        rotation='10 MB',  # Log rotation based on file size
        serialize=True,
    )

    logger.debug(f'Logger set up with log level: {log_level}')
    if log_file:
        logger.debug(f'Log file: {log_file}')
