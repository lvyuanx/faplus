#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: redis_cache.py
Author: lvyuanxiang
Date: 2024/11/26 15:04:27
Description: Redis 缓存实现类
"""
import logging
import asyncio
from typing import Any, Optional

from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

from faplus.cache.base_cache import BaseCache, FAP_CACHE_DEFAULT_EXPIRE

logger = logging.getLogger(__package__)


class RedisCache(BaseCache):
    """
    Redis 缓存实现类
    """

    def __init__(self, cache_config: dict):
        """
        初始化 Redis 缓存类。

        :param cache_config: 缓存配置字典，必须包含 OPTIONS 字段。
        """
        super().__init__(cache_config)
        options = cache_config.get("OPTIONS")
        if not options:
            raise ValueError("Redis Config Error: 'OPTIONS' field is missing.")
        self.pool: ConnectionPool = self._create_pool(options)

    def _create_pool(self, config: dict) -> ConnectionPool:
        """
        创建 Redis 连接池。

        :param config: 配置字典，包含 HOST, PORT, DB 等信息。
        :return: 创建的 Redis 连接池。
        """
        host = config.get("HOST", "127.0.0.1")
        port = config.get("PORT", 6379)
        db = config.get("DB", 0)
        password = config.get("PASSWORD", None)
        decode_responses = config.get("DECODE_RESPONSES", True)
        max_connections = config.get("MAX_CONNECTIONS", 20)
        encoding = config.get("ENCODING", "utf-8")

        if not isinstance(host, str) or not isinstance(port, int) or not isinstance(db, int):
            raise ValueError("Invalid Redis connection parameters.")

        return ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=decode_responses,
            max_connections=max_connections,
            encoding=encoding
        )

    @property
    def client(self) -> Redis:
        """
        获取 Redis 客户端。

        :return: Redis 客户端实例。
        """
        return Redis(connection_pool=self.pool)
    
    async def ping(self) -> bool:
        
        return await self.client.ping()

    async def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """
        获取缓存中的值。

        :param key: 缓存键。
        :param default: 如果键不存在时返回的默认值。
        :return: 缓存值或默认值。
        """
        client = self.client
        try:
            return await client.get(key) or default
        except Exception as e:
            logger.error("Redis get operation failed", exc_info=True)
            return default

    async def set(self, key: str, value: Any, expire: Optional[int] = FAP_CACHE_DEFAULT_EXPIRE) -> None:
        """
        设置缓存值。

        :param key: 缓存键。
        :param value: 缓存值。
        :param expire: 过期时间（秒），默认无过期时间。
        :return: 操作是否成功。
        """
        client = self.client
        try:
            return await client.set(key, value, ex=expire)
        except Exception as e:
            logger.error("Redis set operation failed", exc_info=True)
            return False

    async def delete(self, key: str) -> bool:
        """
        删除缓存键。

        :param key: 要删除的键。
        :return: 操作是否成功。
        """
        client = self.client
        try:
            return await client.delete(key) > 0
        except Exception as e:
            logger.error("Redis delete operation failed", exc_info=True)
            return False

    async def close(self):
        """
        关闭连接池，释放资源。
        """
        try:
            await self.pool.disconnect(inuse_connections=True)
        except Exception as e:
            logger.error(
                "Failed to close Redis connection pool", exc_info=True)
