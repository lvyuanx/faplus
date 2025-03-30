# -*- coding: utf-8 -*-

import logging.config
import os

from faplus.core import settings


def load_logging_cfg():
    logging_cfg = settings.LOGGING

    assert logging_cfg is None or isinstance(
        logging_cfg, dict
    ), "logging_cfg must be a dict, but got {}".format(type(logging_cfg))

    if not logging_cfg:
        from .default_config import LOGGING
        logging_cfg = LOGGING

    return logging_cfg


def init_logging():

    # 加载配置
    logging.config.dictConfig(load_logging_cfg())
