# -*- coding: utf-8 -*-
import logging
import sys

# 颜色代码
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m',      # 靑 (Cyan)
        'INFO': '\033[32m',       # 绿 (Green)
        'WARNING': '\033[33m',    # 黄 (Yellow)
        'ERROR': '\033[31m',      # 红 (Red)
        'CRITICAL': '\033[41m',   # 红底 (Red Background)
    }
    RESET = '\033[0m'

    def format(self, record):
        # 复制一份 record 避免影响其他 handler
        import copy
        record_copy = copy.copy(record)
        color = self.COLORS.get(record_copy.levelname, self.RESET)
        record_copy.levelname = f"{color}{record_copy.levelname}{self.RESET}"
        return super().format(record_copy)

# 创建 zzshare 专用 logger
logger = logging.getLogger("zzshare")

# 默认配置（如果用户没有配置日志，则输出到 stderr）
def _init_logger():
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

# 暴露给用户的快捷设置方法
def set_level(level):
    """
    设置 zzshare 的日志级别
    :param level: 可以是 logging.DEBUG, logging.INFO, 'DEBUG', 'INFO' 等
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    
    # 如果尚未初始化 handlers，先初始化一个默认的
    if not logger.handlers:
        _init_logger()
        
    logger.setLevel(level)

# 默认初始化一次（设置级别为 INFO，保证错误能按标准格式输出）
_init_logger()
logger.setLevel(logging.INFO)
