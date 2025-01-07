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

from faplus.utils import StatusCodeEnum, get_setting_with_default
from faplus.utils import app_util

logger = logging.getLogger(__package__)

status_code_dict = {404: StatusCodeEnum.请求不存在}

end_format = "*" * 15 + "{url}" + "*" * 15 + "\n"


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # 请求前的日志记录
        content_type = request.headers.get("Content-Type", "")
        method = request.method
        path = request.url.path
        logger.info(f"Request: 【{method}】; content-type:{content_type}; url:{path}")
        try:
            if get_setting_with_default("DEBUG", True):
                with app_util.Timer():
                    return await call_next(request)
            return await call_next(request)
        except Exception as e:
            logger.error("An error occurred during request processing", exc_info=True)
            raise e
        finally:
            logger.info(end_format.format(url=path))
