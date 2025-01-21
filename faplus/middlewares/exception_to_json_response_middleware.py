#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: exception_to_json_response_middleware.py
Author: lvyuanxiang
Date: 2024/11/19 15:56:06
Description: 异常转json数据
"""


from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import logging
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from faplus.view import Response as ApiResponse


logger = logging.getLogger(__package__)


class ExceptionToJsonResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            return await call_next(request)
        except ResponseValidationError as e:
            logger.error("HTTP_422_UNPROCESSABLE_ENTITY", exc_info=True)
            return JSONResponse(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": e.errors()},
            )
        except Exception as e:
            logger.error(f"", exc_info=True)
            return Response(
                ApiResponse.fail("500", "服务器错误").json(),
                headers={"Content-Type": "application/json"},
            )
