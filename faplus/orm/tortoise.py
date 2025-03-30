#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: mysql.py
Author: lvyuanxiang
Date: 2024/11/13 10:18:18
Description: 使用mysql数据库
"""
import importlib
import inspect
import logging

from tortoise import Model

from faplus.core import settings

logger = logging.getLogger("FAPlus")

USERNAME = settings.DB_USERNAME
PASSWORD = settings.DB_PASSWORD
HOST = settings.DB_HOST
PORT = settings.DB_PORT
DATABASE = settings.DB_DATABASE
ENGINE = settings.DB_ENGINE
CHARSET = settings.DB_CHARSET
TIMEZONE = settings.DB_TIMEZONE
MAXSIZE = settings.DB_MAXSIZE
MINSIZE = settings.DB_MINSIZE
GENERATE_SCHEMAS = settings.DB_GENERATE_SCHEMAS
INSERTAPPS = settings.FAP_INSERTAPPS
DEBUG = settings.DEBUG


def has_model_subclasses(module):
    for _, obj in inspect.getmembers(module):
        # 判断对象是否是类，并且是 Model 的子类
        if obj is not Model and inspect.isclass(obj) and issubclass(obj, Model):
            return True
    return False


def get_models():

    # 不允许app名称相同
    apps = []
    for app in INSERTAPPS:
        app_name = app.rsplit(".")[-1]
        if app_name in apps:
            raise RuntimeError(f"{app_name} app is already in INSERTAPPS")

    models = []
    for app in INSERTAPPS:
        try:
            model_str = f"{app}.models"
            module = importlib.import_module(model_str)
            if has_model_subclasses(module):
                models.append(model_str)
        except ModuleNotFoundError:
            logger.info(f"{app} models not found")
            pass
        except Exception:
            logger.error("Failed to import models from %s" % app, exc_info=True)

    return models


# Tortoise ORM 配置
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",  # MySQL or Mariadb
            "credentials": {
                "host": HOST,
                "port": PORT,
                "user": USERNAME,
                "password": PASSWORD,
                "database": DATABASE,
                "minsize": MINSIZE,
                "maxsize": MAXSIZE,
                "charset": CHARSET,
                "echo": True,
            },
        }
    },
    "apps": {
        "models": {
            "models": ["aerich.models"] + get_models(),
            "default_connection": "default",
        }
    },
    "use_tz": False,  # 建议不要开启，不然存储日期时会有很多坑，时区转换在项目中手动处理更稳妥。
    "timezone": TIMEZONE,
}
