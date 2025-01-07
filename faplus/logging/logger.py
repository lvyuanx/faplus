# -*- coding: utf-8 -*-

import logging.config
import os

from faplus.utils import get_setting_with_default


class AiomysqlFilter(logging.Filter):
    """tortoise.db_client 和 aiomysql重复，需要去除冗余输出"""

    def filter(self, record):
        return not record.name.startswith("aiomysql")


class ProjectFilter(logging.Filter):
    """tortoise.db_client 和 aiomysql重复，需要去除冗余输出"""

    PROJECT_APP_PACKAGES = get_setting_with_default("PROJECT_APP_PACKAGES")

    def filter(self, record):
        # 只允许PROJECT_APP_PACKAGES的包前置缀，否则不输出
        name = record.name
        return self.PROJECT_APP_PACKAGES and any(
            name.startswith(pkg) for pkg in self.PROJECT_APP_PACKAGES
        )


def load_logging_cfg():
    log_level = get_setting_with_default("LOG_LEVEL")
    log_dir = get_setting_with_default("LOG_DIR")
    logging_cfg = get_setting_with_default("LOGGING")

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

    if not logging_cfg:
        logging_cfg = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "detailed": {
                    "format": "[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s"
                },
                "simple": {
                    "format": "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s"
                },
            },
            "filters": {
                "aiomysql_filter": {
                    "()": f"{__name__}.AiomysqlFilter",
                },
                "project_filter": {
                    "()": f"{__name__}.ProjectFilter",
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
                }
            },
        }

    return logging_cfg


def init_logging():

    # 加载配置
    logging.config.dictConfig(load_logging_cfg())
