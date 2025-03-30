#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: base_cache.py
Author: lvyuanxiang
Date: 2024/11/26 14:33:21
Description: 缓存基类
"""

from faplus.utils import settings

FAP_CACHE_DEFAULT_EXPIRE = settings.FAP_CACHE_DEFAULT_EXPIRE

class BaseCache(object):
    """缓存基类"""

    def __init__(self, cache_config: dict):
        self.cache_config = cache_config
        self._prefix = cache_config.get("PREFIX")

    @property
    def perfix(self):
        return self._prefix

    async def set(self, key: str, value: str, expire: int = FAP_CACHE_DEFAULT_EXPIRE) -> None:
        """设置缓存"""
        raise NotImplementedError("cache set method must be implemented")

    async def get(self, key: str, default: str = None) -> str | None:
        """获取缓存"""
        raise NotImplementedError("cache get method must be implemented")

    async def get_keys(self, prefix: str) -> list[str]:
        """获取缓存key"""
        raise NotImplementedError("cahce get_keys method must be implemented")

    async def delete(self, key: str | list[str]) -> None:
        """删除缓存"""
        raise NotImplementedError("cache delete method must be implemented")

    async def clear(self) -> None:
        """清空缓存"""
        raise NotImplementedError("cache clear method must be implemented")

    async def ping(self) -> bool:
        """检查缓存是否可用"""
        raise NotImplementedError("cache ping method must be implemented")
