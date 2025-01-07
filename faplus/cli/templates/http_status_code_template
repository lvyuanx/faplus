#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: http_status_code.py
Author: lvyuanxiang
Date: 2024/11/25 16:11:13
Description: 全局通用异常码枚举(接口的异常码，请在接口内定义，并使用make_code方法返回。)
"""

from enum import Enum
from faplus.http_status_code import CommonStatusCodeEnum as SysCommonCodeEnum
from faplus.auth.http_status_code import ComonStatusCodeEnum as AuthCommonCodeEnum


def merge_enums(*enums, name: str):
    # 创建一个新的字典，存储合并后的枚举成员
    merged_enum_dict = {}
    for enum in enums:
        for name, member in enum.__members__.items():
            merged_enum_dict[name] = member.value
    # 使用type动态创建一个新的枚举类
    return Enum(name, merged_enum_dict)


# 动态合并枚举类
StatusCodeEnum = merge_enums(SysCommonCodeEnum, AuthCommonCodeEnum, name="CommonStatusCodeEnum")
