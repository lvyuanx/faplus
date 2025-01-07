#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: menory_cache.py
Author: lvyuanxiang
Date: 2024/11/26 16:44:45
Description: 内存缓存实现类
"""

import asyncio
import time
from typing import Any, Optional

from faplus.cache.base_cache import BaseCache, FAP_CACHE_DEFAULT_EXPIRE


class MemoryCache(BaseCache):
    """基于内存的缓存实现"""

    def __init__(self, cache_config: dict):
        """
        初始化内存缓存
        :param cache_config: 缓存配置，包含前缀等
        """
        super().__init__(cache_config)
        self._store = {}  # 内存缓存存储
        self._lock = asyncio.Lock()  # 异步锁，确保线程安全

    async def set(self, key: str, value: Any, expire: Optional[int] = FAP_CACHE_DEFAULT_EXPIRE) -> None:
        """
        设置缓存
        :param key: 缓存键
        :param value: 缓存值
        :param expire: 过期时间（秒），None（永久有效）
        """
        async with self._lock:
            expire_at = time.time() + expire if expire else None
            self._store[key] = {"value": value, "expire_at": expire_at}

    async def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """
        获取缓存
        :param key: 缓存键
        :param default: 如果键不存在返回的默认值
        :return: 缓存值或默认值
        """
        async with self._lock:
            data = self._store.get(key)
            if not data:
                return default
            # 检查是否过期
            if data["expire_at"] and data["expire_at"] < time.time():
                await self.delete(key)  # 删除过期缓存
                return default
            return data["value"]

    async def get_keys(self, prefix: str) -> list[str]:
        """
        获取指定前缀的所有缓存键
        :param prefix: 键前缀
        :return: 符合前缀的键列表
        """
        async with self._lock:
            return [key for key in self._store.keys() if key.startswith(prefix)]

    async def delete(self, key: str | list[str]) -> None:
        """
        删除缓存
        :param key: 单个键或键列表
        """
        async with self._lock:
            if isinstance(key, str):
                self._store.pop(key, None)
            elif isinstance(key, list):
                for k in key:
                    self._store.pop(k, None)

    async def clear(self) -> None:
        """
        清空所有缓存
        """
        async with self._lock:
            self._store.clear()

    async def ping(self) -> bool:
        """
        检查缓存是否可用
        :return: 总是返回 True，表示内存缓存可用
        """
        return True
