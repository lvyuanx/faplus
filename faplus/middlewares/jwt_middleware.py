#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: login_middleware.py
Author: lvyuanxiang
Date: 2024/11/19 15:56:19
Description: 登录中间件
"""
import logging

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from faplus.utils import (
    StatusCodeEnum,
    get_setting_with_default,
    Response as ApiResponse
)
from faplus.utils import token_util
from faplus.auth.utils import user_util
from faplus.cache import cache


logger = logging.getLogger(__package__)

FAP_TOKEN_TAG = get_setting_with_default("FAP_TOKEN_TAG")


class JwtMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        state = request.state
        if not state.is_static and not state.is_whitelist:
            # 获取header中的token
            token = request.headers.get(FAP_TOKEN_TAG)
            payload = await token_util.verify_token(token)
            if not payload:
                logger.error("token验证失败")
                error_code = StatusCodeEnum.用户未登录
                return Response(
                    ApiResponse.fail(error_code.value, error_code.name).json(),
                    headers={"Content-Type": "application/json"},
                )

            try:
                user_dict = await user_util.get_user_info(id=payload.get("uid"))
            except Exception:
                logger.debug("", exc_info=True)
                user_dict = None
            if not user_dict:
                logger.error("TOKEN无效")
                error_code = StatusCodeEnum.TOKEN无效
                return Response(
                    ApiResponse.fail(error_code.value, error_code.name).json(),
                    headers={"Content-Type": "application/json"},
                )
            request.state.user_info = user_dict
            request.state.uid = user_dict["id"]

        return await call_next(request)
