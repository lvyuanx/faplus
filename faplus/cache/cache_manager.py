#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: cache_manager.py
Author: lvyuanxiang
Date: 2024/11/26 13:47:48
Description: 缓存管理器
"""
import importlib
import logging

from .base_cache import BaseCache, FAP_CACHE_DEFAULT_EXPIRE
from faplus.utils import settings

logger = logging.getLogger(__package__)


class CacheManager(object):

    def __init__(self, cache_config_dict: dict | None):
        self.cache_obj_dict: dict[str, BaseCache] = {}  # 缓存对象字典
        for name, config in cache_config_dict.items():
            cache_backend = self.init_backend(config)
            self.cache_obj_dict[name] = cache_backend

    def all_backend(self) -> list[BaseCache]:
        return list(self.cache_obj_dict.values())

    def init_backend(self, config: dict) -> BaseCache:
        backend = config["BACKEND"]
        module_str, clazz_str = backend.rsplit(".", 1)
        module = importlib.import_module(module_str)
        cache_clazz = getattr(module, clazz_str, None)
        if not cache_clazz:
            raise RuntimeError(f"cache backend {backend} not found")
        return cache_clazz(config)

    def get_backend(self, backend: str = "default") -> BaseCache:
        if backend not in self.cache_obj_dict:
            raise RuntimeError(f"cache backend {backend} not found")
        return self.cache_obj_dict[backend]

    async def _execute_cache_operation(
        self, method: str, key: str, *args, backend: str = "default"
    ):
        assert key and isinstance(key, str), "key must be a string"
        cache = self.get_backend(backend)
        try:
            method_func = getattr(cache, method)
            prefix = cache.perfix  # key前缀
            result = await method_func(f"{prefix}{key}", *args)
            return result
        except Exception:
            logger.error(f"Error executing cache operation '{method}'", exc_info=True)
            return None

    async def set(
        self,
        key: str,
        value: str,
        expire: int = FAP_CACHE_DEFAULT_EXPIRE,
        backend: str = "default",
    ) -> None:
        """保存

        :param key: 缓存的key
        :param value: 缓存的值
        :param expire: 过期时间
        :param nx: nx, defaults to False
        """
        if (
            not isinstance(key, str)
            or not isinstance(value, str)
            or (expire and not isinstance(expire, int))
        ):
            raise ValueError("Invalid input types for key, value, or expire")
        await self._execute_cache_operation("set", key, value, expire, backend=backend)

    async def get(self, key: str, backend: str = "default") -> str | None:
        """获取缓存

        :param key: 缓存的key
        :param backend: 缓存的backend, defaults to "default"
        :return: 缓存的值
        """
        return await self._execute_cache_operation("get", key, backend=backend)

    async def get_keys(self, prefix: str, backend: str = "default") -> list[str]:
        """获取缓存key

        :param prefix: 缓存key的前缀
        :param backend: 缓存的backend, defaults to "default"
        :return: 缓存key列表
        """
        return await self._execute_cache_operation("get_keys", prefix, backend=backend)

    async def delete(self, key: str, backend: str = "default") -> None:
        """删除缓存

        :param key: 缓存的key
        :param backend: 缓存的backend, defaults to "default"
        """
        await self._execute_cache_operation("delete", key, backend=backend)

    async def clear(self, backend: str = "default") -> None:
        """清空缓存

        :param backend: 缓存的backend, defaults to "default"
        """
        await self._execute_cache_operation("clear", backend=backend)

    async def ping(self, backend: str = "default") -> bool:
        """检查缓存是否可用

        :param backend: 缓存的backend, defaults to "default"
        :return: 是否可用
        """
        cache = self.get_backend(backend)
        return await cache.ping()


FAP_CACHE_CONFIG = settings.FAP_CACHE_CONFIG

cache = CacheManager(FAP_CACHE_CONFIG)
