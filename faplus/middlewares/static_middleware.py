# -*-coding:utf-8 -*-

"""
# File       : static_middleware.py
# Time       : 2025-01-05 20:59:10
# Author     : lyx
# version    : python 3.11
# Description: 静态资源中间件
"""
import logging

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from faplus import const
from faplus.utils import get_setting_with_default
from faplus.cache import cache


logger = logging.getLogger(__package__)


FAP_STATIC_URL = get_setting_with_default("FAP_STATIC_URL")


async def is_static(url: str) -> bool:
    """判断是否在白名单中"""
    if await cache.get(url):
        # 增加对过期时间的缓存
        await cache.set(const.STATIC_CK.format(url=url), "1", 60 * 60 * 24)
        return True
    if url.startswith(FAP_STATIC_URL):
        await cache.set(const.STATIC_CK.format(url=url), "1", 60 * 60 * 24)
        return True
    return False


class StaticMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        path = request.url.path

        request.state.is_static = await is_static(path)

        return await call_next(request)
