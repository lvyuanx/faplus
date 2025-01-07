#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: example_adapater.py
Author: lvyuanxiang
Date: 2024/11/12 16:18:55
Description: 接口模板适配器
"""


from faplus.utils.config_util import StatusCodeEnum


def success() -> dict:
    return {
        "code": StatusCodeEnum.请求成功,
        "msg": StatusCodeEnum.请求成功.name,
        "data": None
    }


def error(code: str, msg: str) -> dict:
    return {
        "code": code,
        "msg": msg,
        "data": None
    }