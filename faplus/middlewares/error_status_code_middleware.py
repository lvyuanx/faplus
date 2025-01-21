#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: error_status_code_middleware.py
Author: lvyuanxiang
Date: 2024/11/19 15:56:06
Description: 日志中间件
"""


from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import logging

from faplus.utils import StatusCodeEnum, Response as ApiResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_200_OK

logger = logging.getLogger(__package__)


def get_by_code(code: str):
    """根据状态码获取状态码名称
    :param code: 状态码
    :return: 枚举
    """

    for _, member in StatusCodeEnum.__members__.items():
        if member.value == code:
            return member
    return None


class ErrorStatusCodeMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        res = await call_next(request)
        status_code = res.status_code
        if status_code in [HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY]:
            return res
        else:
            logger.error(f"Response: {status_code}")
            error_enum = get_by_code(str(status_code))
            if error_enum:
                data = ApiResponse.fail(error_enum.value, error_enum.name)
            else:
                data = ApiResponse.fail(str(status_code), "服务器错误")
            return Response(
                data.json(),
                headers={"Content-Type": "application/json"},
            )
