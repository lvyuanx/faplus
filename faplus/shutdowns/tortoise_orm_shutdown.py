#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: tortoise_orm_startup.py
Author: lvyuanxiang
Date: 2025/01/03 14:33:22
Description: tortoise orm启动器
"""
from tortoise import Tortoise

def tortoise_orm_close_event(**kwargs):

    async def do():
        await Tortoise.close_connections()
    return do