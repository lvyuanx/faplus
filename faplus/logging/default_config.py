import os 

from faplus.utils import settings

log_level = settings.LOG_LEVEL
log_dir = settings.LOG_DIR
logging_cfg = settings.LOGGING

assert log_level.upper() in (
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
), f"logger level mast be DEBUG, INFO, WARNING, ERROR, CRITICAL, but got {log_level}"

assert log_dir, f"log_dir is None"

assert logging_cfg is None or isinstance(
    logging_cfg, dict
), "logging_cfg must be a dict, but got {}".format(type(logging_cfg))


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d][%(funcName)s][%(levelname)s] - %(message)s"
        },
        "simple": {
            "format": "[%(asctime)s][%(filename)s:%(lineno)d][%(funcName)s][%(levelname)s] - %(message)s"
        },
    },
    "filters": {
        "aiomysql_filter": {
            "()": f"faplus.logging.log_filter.AiomysqlFilter",
        },
        "project_filter": {
            "()": f"faplus.logging.log_filter.ProjectFilter",
        },
    },
    "handlers": {
        "all": {  # 记录所有日志
            "level": "DEBUG",
            "class": "faplus.logging.log_handler.MultiprocessTimeHandler",
            "file_path": log_dir,
            "suffix": "%Y-%m-%d-all",
            "formatter": "detailed",
            "backup_count": 30,
            "encoding": "utf-8",
            "filters": ["aiomysql_filter"],
        },
        "media": {  # 记录项目日志
            "level": "DEBUG",
            "class": "faplus.logging.log_handler.MultiprocessTimeHandler",
            "file_path": log_dir,
            "suffix": "%Y-%m-%d-media",
            "formatter": "detailed",
            "backup_count": 30,
            "encoding": "utf-8",
        },
        "project": {  # 记录项目日志
            "level": "DEBUG",
            "class": "faplus.logging.log_handler.MultiprocessTimeHandler",
            "file_path": log_dir,
            "suffix": "%Y-%m-%d-project",
            "formatter": "detailed",
            "backup_count": 30,
            "encoding": "utf-8",
            "filters": ["aiomysql_filter", "project_filter"],
        },
        "error": {  # 只记录错误日志
            "level": "ERROR",
            "class": "faplus.logging.log_handler.MultiprocessTimeHandler",
            "file_path": log_dir,
            "suffix": "%Y-%m-%d-error",
            "formatter": "detailed",
            "backup_count": 30,
            "encoding": "utf-8",
            "filters": ["aiomysql_filter"],
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "filters": ["aiomysql_filter"],
        },
    },
    "loggers": {
        "": {
            "handlers": ["all", "console", "error", "project"],
            "level": log_level,
            "propagate": True,
        },
        "media": {
            "handlers": ["media"],
            "level": log_level,
            "propagate": True,
        },
    },
}
