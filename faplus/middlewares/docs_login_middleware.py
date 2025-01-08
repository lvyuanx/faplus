# -*-coding:utf-8 -*-

"""
# File       : docs_login_middleware.py
# Time       : 2025-01-08 21:02:20
# Author     : lyx
# version    : python 3.11
# Description: 在线文档登录拦截器
"""
import logging

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from faplus.utils import get_setting_with_default
from faplus.auth.utils import user_util
from faplus.utils import token_util

FAP_DOCS_URL = get_setting_with_default("FAP_DOCS_URL")
FAP_REDOC_URL = get_setting_with_default("FAP_REDOC_URL")
DEBUG = get_setting_with_default("DEBUG")

logger = logging.getLogger(__package__)

class DocsLoginMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        
        path = request.url.path
        if not path.startswith(FAP_DOCS_URL) and not path.startswith(FAP_REDOC_URL):
            return await call_next(request)
        
        tk = request.cookies.get("token")
        if tk and await token_util.verify_token(tk):  # 验证token
            return await call_next(request)
        
        query = request.query_params
        username = query.get("username")
        password = query.get("password")
        if username and password:
            try:
                user = await user_util.authenticate_user(username=username, password=password)
                if user:
                    token = await token_util.create_token(user)
                    response = await call_next(request)
                    response.set_cookie(key="token", value=token, httponly=DEBUG)
                    return response
            except Exception as e:
                logging.warning("", exc_info=True)
        
        return Response(status_code=401)

        