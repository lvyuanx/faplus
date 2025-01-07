#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: cache_loader.py
Author: lvyuanxiang
Date: 2024/11/26 15:34:48
Description: 缓存加载器
"""


from typing import Union

from fastapi import FastAPI


def loader(app: Union[FastAPI, None] = None) -> Union[FastAPI, None]:
    from faplus.cache import cache

    return app
