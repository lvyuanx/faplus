#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: login_middleware.py
Author: lvyuanxiang
Date: 2024/11/19 15:56:19
Description: 登录中间件
"""
import logging
from typing import Union, Callable, Dict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from faplus.utils import (
    StatusCodeEnum,
    settings,
    Response as ApiResponse
)
from faplus.utils import token_util
from faplus.auth.utils import user_util, guest_util
from faplus.cache import cache
from faplus import const

logger = logging.getLogger(__package__)

FAP_TOKEN_TAG = settings.FAP_TOKEN_TAG
FAP_TOKEN_SOURCE = settings.FAP_TOKEN_SOURCE
TokenSourceEnum = const.TokenSourceEnum
GUEST_USER_DICT = guest_util.generate_user_dict()

# 定义类型别名
TokenHandler = Callable[[Request], Union[None, str]]

def _token_handle() -> TokenHandler:
    handle: Dict[TokenSourceEnum, TokenHandler] = {
        TokenSourceEnum.Cookie: lambda request: request.cookies.get(FAP_TOKEN_TAG),
        TokenSourceEnum.Header: lambda request: request.headers.get(FAP_TOKEN_TAG),
        TokenSourceEnum.Query: lambda request: request.query_params.get(FAP_TOKEN_TAG),
        TokenSourceEnum.Body : lambda request: request.json().get(FAP_TOKEN_TAG) if request.json() else None,
   }
    try:
        return handle[FAP_TOKEN_SOURCE]
    except Exception:
        logger.error("token处理器获取失败", exc_info=True)
    
    return lambda request: None

token_handle = _token_handle()
    

def get_token(request: Request) -> str | None:
    try:
        return token_handle(request)
    except Exception:
        logger.error("token获取失败", exc_info=True)


class JwtMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        state = request.state
        if not state.is_static and not state.is_whitelist:            
            # 获取header中的token
            token = get_token(request)
            payload = await token_util.verify_token(token)
            if not payload:
                logger.error("token验证失败")
                error_code = StatusCodeEnum.用户未登录
                return Response(
                    ApiResponse.fail(error_code.value, error_code.name).json(),
                    headers={"Content-Type": "application/json"},
                )

            is_gest = payload.get("is_gest")
            if is_gest:
                gest_username = payload.get("username")
                user = GUEST_USER_DICT.get(gest_username)
                if not user:
                    logger.error(f"GestUser:{gest_username}不存在")
                    error_code = StatusCodeEnum.TOKEN无效
                    return Response(
                        ApiResponse.fail(error_code.value, error_code.name).json(),
                        headers={"Content-Type": "application/json"},
                    )
                user_dict = user.to_dict()
            else:
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
            request.state.is_gest = is_gest

        return await call_next(request)
