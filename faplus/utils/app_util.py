#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: app_util.py
Author: lvyuanxiang
Date: 2025/01/03 14:25:23
Description: app 工具类
"""
import logging
import time
from functools import wraps

logger = logging.getLogger(__package__)

class Timer:
    
    def __init__(self, target: str = None) -> None:
        self.target = target
    
    def __enter__(self):
        # 在进入 with 代码块时记录当前时间
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 在退出 with 代码块时计算执行时间
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        logger.debug(f"{self.target} Execution time: {self.duration} seconds")
        return False

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录开始时间
        result = func(*args, **kwargs)  # 执行原始函数
        end_time = time.time()  # 记录结束时间
        duration = end_time - start_time
        logger.debug(f"Execution time of {func.__name__}: {duration:.4f} seconds")
        return result
    return wrapper

