#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: cache_ping_startup.py
Author: lvyuanxiang
Date: 2025/01/03 15:17:54
Description: 缓存ping
"""

def cache_ping_event(**kwargs):
    
    async def do():
        from faplus.cache import cache
        await cache.ping()
    
    return do
