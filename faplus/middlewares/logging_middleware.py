#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: logging_middleware.py
Author: lvyuanxiang
Date: 2024/11/19 15:56:06
Description: 日志中间件
"""


from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import logging

from faplus.utils import get_setting_with_default
from faplus.utils import app_util

logger = logging.getLogger(__package__)

DEBUG = get_setting_with_default("DEBUG", True)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # 请求前的日志记录
        method = request.method
        path = request.url.path
        if DEBUG:
            with app_util.Timer(f"{method} {path}"):
                return await call_next(request)
        return await call_next(request)
