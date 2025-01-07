# -*-coding:utf-8 -*-

"""
# File       : content_type_startup.py
# Time       : 2025-01-05 23:26:21
# Author     : lyx
# version    : python 3.11
# Description: 启动时初始化内容类型
"""
import importlib

from faplus.utils import get_setting_with_default
from tortoise.models import Model
from faplus.models import ContentType


def content_type_register_event(**kwargs):

    async def do():
        FAP_INSERTAPPS = get_setting_with_default("FAP_INSERTAPPS")
        model_dict = {}
        for app in FAP_INSERTAPPS:
            try:
                app_models = importlib.import_module(f"{app}.models")
            except ModuleNotFoundError:
                continue

            # 获取所有模型
            for model in app_models.__dict__.values():
                if isinstance(model, type) and issubclass(model, Model):
                    model_dict[app.rsplit(".")[-1]] = model.__name__

        for app, model in model_dict.items():
            await ContentType.get_or_create(
                app_label=app,
                model=model,
            )

    return do
