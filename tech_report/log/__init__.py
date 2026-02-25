# logger_config.py
import sys
from loguru import logger
import os

# 移除默认的处理器（避免重复输出）
logger.remove()

# 定义日志格式
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> | <level>{message}</level>"

# 配置控制台输出
logger.add(
    sys.stderr,
    format=log_format,
    level="DEBUG",  # 开发时可设为DEBUG，生产环境建议设为INFO或WARNING
    colorize=True,
    backtrace=True,
    diagnose=True
)

# 配置文件输出（自动轮转）
logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    rotation="00:00",        # 每天零点创建新文件
    retention="30 days",     # 保留30天
    compression="zip",       # 压缩旧日志
    level="INFO",
    format=log_format,
    encoding="utf-8",
    enqueue=True             # 多进程安全
)

# 配置错误日志单独文件
logger.add(
    "logs/error_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="30 days",
    compression="zip",
    level="ERROR",
    format=log_format,
    encoding="utf-8",
    enqueue=True
)

# 可选：根据环境变量调整日志级别
if os.getenv("ENV") == "production":
    # 生产环境降低控制台输出级别
    logger.remove()  # 重新配置
    logger.add(sys.stderr, level="WARNING", format=log_format)
    # 文件配置不变...