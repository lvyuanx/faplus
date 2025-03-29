# -*-coding:utf-8 -*-

"""
# File       : log_filter.py
# Time       : 2025-03-29 21:49:29
# Author     : lyx
# version    : python 3.11
# Description: 日志过滤器
"""
import logging

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
