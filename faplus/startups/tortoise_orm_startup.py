#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: tortoise_orm_startup.py
Author: lvyuanxiang
Date: 2025/01/03 14:33:22
Description: tortoise orm启动器
"""
from tortoise import Tortoise

from faplus.orm.tortoise import GENERATE_SCHEMAS, TORTOISE_ORM, ENGINE


def tortoise_orm_init_event(**kwargs):

    async def do():
        if ENGINE:

            # 初始化 Tortoise ORM
            await Tortoise.init(config=TORTOISE_ORM)

            # 生成数据库表（如果需要）
            if GENERATE_SCHEMAS:
                await Tortoise.generate_schemas()

    return do
