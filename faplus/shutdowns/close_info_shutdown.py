#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: close_info_shutdowns.py
Author: lvyuanxiang
Date: 2024/11/25 10:32:32
Description: 关闭信息
"""
import logging

logger = logging.getLogger(__package__)


def close_info_event(**kwargs):
    async def do():
        logger.info("\n\n》》》》》》》》》》》》》》》》》》》》》》》》》 FastApi Plus 《《《《《《《《《《《《《《《《《《《《《《《《《\n\n")
    
    return do