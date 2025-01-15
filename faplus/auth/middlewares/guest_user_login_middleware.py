# -*-coding:utf-8 -*-

"""
# File       : gest_user_login_middleware.py
# Time       : 2025-01-05 15:35:15
# Author     : lyx
# version    : python 3.11
# Description: 访客登录中间件
"""

import logging
from typing import Any, Union, Callable, Dict
import json
from fastapi import responses

from starlette.datastructures import MutableHeaders
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from faplus.utils import get_setting_with_default, token_util
from faplus.auth.utils import guest_util
from faplus import const as faplus_const

logger = logging.getLogger(__package__)
TokenSourceEnum = faplus_const.TokenSourceEnum
FAP_TOKEN_TAG = get_setting_with_default("FAP_TOKEN_TAG")
DEBUG = get_setting_with_default("DEBUG")
FAP_GEST_USERS_LOGIN_URL = get_setting_with_default("FAP_GEST_USERS_LOGIN_URL")
FAP_TOKEN_SOURCE = get_setting_with_default("FAP_TOKEN_SOURCE")

GUEST_USER_DICT = guest_util.generate_user_dict()

def get_url(url: str):
    return url.replace(FAP_GEST_USERS_LOGIN_URL, "")

def _set_cookie(request: Request, token: str) -> Response:
    response = RedirectResponse(url=get_url(request.url.path), status_code=302)
    response.set_cookie(key=FAP_TOKEN_TAG, value=token, httponly=DEBUG)
    return response

def _set_header(request: Request, token: str) -> Response:
    path = request.url.path
    response = RedirectResponse(url=get_url(path), status_code=302)
    response.headers[FAP_TOKEN_TAG] = token
    
    return response


def _set_query(request: Request, token: str):
    path = request.url.path
    return RedirectResponse(url=f"{get_url(path)}?{FAP_TOKEN_TAG}={token}", status_code=302)
    
def _set_body(request: Request, token: str):
    # 同样，这里假设 body 是一个可以被序列化的字典。
    # 如果不是，则需要根据实际情况调整。
    try:
        body = request.json()
        if isinstance(body, dict):
            body[FAP_TOKEN_TAG] = token
        else:
            logger.warning("无法将token添加到非字典类型的响应体中")
        return RedirectResponse(url=get_url(request.url.path), content=json.dumps(body), status_code=302)
    except Exception as e:
        logger.error(f"设置响应体中的token失败: {e}", exc_info=True)

# 定义类型别名
TokenHandler = Callable[[Request, str], Union[None, RedirectResponse]]
def _token_handle() -> TokenHandler:
    handle: Dict[TokenSourceEnum, TokenHandler] = {
        TokenSourceEnum.Cookie: lambda request, token: _set_cookie(request, token),
        TokenSourceEnum.Header: lambda request, token: _set_header(request, token),
        TokenSourceEnum.Query: lambda request, token: _set_query(request, token),
        TokenSourceEnum.Body : lambda request, token: _set_body(request, token),
   }
    try:
        return handle[FAP_TOKEN_SOURCE]
    except Exception:
        logger.error("token处理器获取失败", exc_info=True)
    
    return lambda request, token: None

token_handle = _token_handle()

    


class GuestUserLoginMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # 获取url
        path = request.url.path
        if not path.endswith(FAP_GEST_USERS_LOGIN_URL):
            return await call_next(request)

        username = request.query_params.get("username")
        password = request.query_params.get("password")
 
        if not username or not password:
            return Response(status_code=404)
        
        user = GUEST_USER_DICT.get(username)
        if not user or user.password != password:
            return Response(status_code=404)
        
        token = await token_util.create_token({"username": user.username, "is_gest": True})
        res = token_handle(request, token)
        print(res)
        if not res:
            return Response(status_code=404)
        return res
        