# -*-coding:utf-8 -*-

"""
# File       : whitelist_middleware.py
# Time       : 2025-01-05 20:59:10
# Author     : lyx
# version    : python 3.11
# Description: 白名单中间件
"""
import logging

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from faplus import const
from faplus.utils import get_setting_with_default
from faplus.cache import cache


logger = logging.getLogger(__package__)

FAP_JWT_WHITES = get_setting_with_default("FAP_JWT_WHITES")
FAP_LOGIN_URL = get_setting_with_default("FAP_LOGIN_URL")
FAP_DOCS_URL = get_setting_with_default("FAP_DOCS_URL")
FAP_REDOC_URL = get_setting_with_default("FAP_REDOC_URL")
FAP_OPENAPI_URL = get_setting_with_default("FAP_OPENAPI_URL")

# 白名单 + 登录地址 + docs地址 + redoc地址 + openapi地址 予以放行
whitelist = FAP_JWT_WHITES + [
    FAP_LOGIN_URL,
    FAP_DOCS_URL,
    FAP_REDOC_URL,
    FAP_OPENAPI_URL,
]


async def is_whitelist(url: str) -> bool:
    """判断是否在白名单中"""
    if await cache.get(url):
        # 增加对过期时间的缓存
        await cache.set(const.WHITELIST_CK.format(url=url), "1", 60 * 60 * 24)
        return True
    for w in whitelist:
        if w == url or (w.endswith("*") and url.startswith(w[:-1])):
            await cache.set(const.WHITELIST_CK.format(url=url), "1", 60 * 60 * 24)
            return True
    return False


class WhitelistMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        path = request.url.path

        request.state.is_whitelist = await is_whitelist(path)

        return await call_next(request)
