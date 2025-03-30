# -*-coding:utf-8 -*-

"""
# File       : content_type_startup.py
# Time       : 2025-01-05 23:26:21
# Author     : lyx
# version    : python 3.11
# Description: 启动时初始化内容类型
"""
import importlib
import inspect

from faplus.utils import settings
from tortoise.models import Model
from faplus.models import ContentType
from collections import defaultdict


def content_type_register_event(**kwargs):

    async def do():
        FAP_INSERTAPPS = settings.FAP_INSERTAPPS
        model_dict = defaultdict(list)
        for app in FAP_INSERTAPPS:
            try:
                app_models = importlib.import_module(f"{app}.models")
            except ModuleNotFoundError:
                continue
            
            for _, obj in inspect.getmembers(app_models):
                # 判断对象是否是类，并且是 Model 的子类
                if obj is not Model and inspect.isclass(obj) and issubclass(obj, Model):
                    model_dict[app.rsplit(".")[-1]].append(obj.__name__)
        
        

        for app, models in model_dict.items():
            for model in models:
                await ContentType.get_or_create(
                    app_label=app,
                    model=model,
                )

    return do
