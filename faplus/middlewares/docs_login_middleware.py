# -*-coding:utf-8 -*-

"""
# File       : docs_login_middleware.py
# Time       : 2025-01-08 21:02:20
# Author     : lyx
# version    : python 3.11
# Description: 在线文档登录拦截器
"""
import logging
import base64

from fastapi import Request, Response, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from faplus.utils import settings
from faplus.auth.utils import user_util
from faplus.utils import token_util

FAP_DOCS_URL = settings.FAP_DOCS_URL
FAP_REDOC_URL = settings.FAP_REDOC_URL
FAP_OPENAPI_URL = settings.FAP_OPENAPI_URL
DEBUG = settings.DEBUG
FAP_TOKEN_TAG = settings.FAP_TOKEN_TAG

logger = logging.getLogger(__package__)

class DocsLoginMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path = request.url.path
        if not path.startswith(FAP_DOCS_URL) and not path.startswith(FAP_REDOC_URL) and not path.startswith(FAP_OPENAPI_URL):
            return await call_next(request)
        
        tk = request.cookies.get(FAP_TOKEN_TAG)
        if tk and token_util.verify_token(tk):
            return await call_next(request)
        
        # 提取Authorization头部
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing credentials"},
                headers={"WWW-Authenticate": "Basic realm='Protected Area'"}
            )
        
        # 验证头部格式
        try:
            scheme, encoded = auth_header.split()
            if scheme.lower() != "basic":
                raise ValueError
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":", 1)
        except (ValueError, UnicodeDecodeError):
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication format",
                headers={"WWW-Authenticate": "Basic"}
            )
        
        if username and password:
            try:
                user = await user_util.authenticate_user(username=username, password=password)
                if user:
                    token = await token_util.create_token({"uid": user["id"]})
                    response = RedirectResponse(url=path, status_code=302)
                    response.set_cookie(key=FAP_TOKEN_TAG, value=token, httponly=DEBUG)
                    return response
            except Exception as e:
                logging.warning("", exc_info=True)
        return Response(status_code=401)

        