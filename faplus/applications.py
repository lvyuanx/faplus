#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: init_api.py
Author: lvyuanxiang
Date: 2024/11/06 11:48:48
Description: 程序入口
"""
import os
import logging
import importlib
from typing import Tuple, Union
from functools import partial

from fastapi.applications import FastAPI
from faplus.core import settings


package = __package__
logger = logging.getLogger(package)


class FastApiPlusApplication(object):

    app: FastAPI = None

    def __init__(self) -> FastAPI:
        os.environ.setdefault("FAP_PACKAGE", __package__)

    @property
    def fastapi_instance(self):

        self.load()

        if not self.app:
            raise RuntimeError("application is None")

        # 注册事件
        self.event_register(self.app)

        # 注册中间件
        self.middleware_register(self.app)

        # 注册websocket
        self.websocket_register(self.app)

        return self.app

    def load(self):
        """系统中的功能使用loader进行加载"""
        loader_lst = [
            "logging_loader",
            "router_loader",
            "cache_loader",
        ]
        try:
            for loader in loader_lst:
                loader_module = importlib.import_module(f"{package}.loaders.{loader}")
                self.app = getattr(loader_module, "loader")(self.app)
        except Exception as e:
            logger.error("fast api plus load error", exc_info=True)
            raise e

    def event_register(self, app: FastAPI):
        """事件注册"""
        startups: list[Union[str, Tuple[str, dict]]] = settings.FAP_STARTUP_FUNCS
        shutdowns: list[Union[str, Tuple[str, dict]]] = settings.FAP_SHUTDOWN_FUNCS

        def add_event(event_name: str, events: list[Union[str, Tuple[str, dict]]]):

            for event in events:
                if isinstance(event, str):
                    func_str = event
                    kwargs = None
                elif isinstance(event, tuple):
                    func_str, kwargs = event
                else:
                    raise ValueError(f"{event_name} {event} is not valid")

                module_name, func_name = func_str.rsplit(".", 1)
                module = importlib.import_module(module_name)
                func = getattr(module, func_name, None)
                assert callable(func), f"{event_name} {func_str} is not callable"

                if kwargs:
                    handler = partial(func, **kwargs)
                else:
                    handler = func
                app.add_event_handler(event_name, handler())

        add_event("startup", startups)
        add_event("shutdown", shutdowns)

    def middleware_register(self, app: FastAPI):
        """中间件注册"""
        middlewares: list[Union[str, Tuple[str, dict]]] = settings.FAP_MIDDLEWARE_CLASSES
        for middleware in middlewares:

            if isinstance(middleware, str):
                module_class = middleware
                kwargs = None
            elif isinstance(middleware, tuple):
                module_class, kwargs = middleware
            else:
                raise ValueError(f"{middleware} is not valid")

            module_name, class_name = module_class.rsplit(".", 1)
            module = importlib.import_module(module_name)
            middleware_cls = getattr(module, class_name, None)
            assert middleware_cls, f"middleware {middleware} is not found"

            if kwargs:
                app.add_middleware(middleware_cls, **kwargs)
            else:
                app.add_middleware(middleware_cls)

    def websocket_register(self, app: FastAPI):
        from .utils import settings

        websocket_routes: list[str] = settings.FAP_WS_CLASSES
        for websocket_route in websocket_routes:
            path, ws_name = websocket_route.rsplit(".", 1)
            module = importlib.import_module(path)
            ws_cls = getattr(module, ws_name, None)
            assert ws_cls, f"{ws_cls} is not found"
            app.router.routes.append(ws_cls())


app: FastAPI = FastApiPlusApplication().fastapi_instance
