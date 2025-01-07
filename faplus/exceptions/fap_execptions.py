#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: fap_execptions.py
Author: lvyuanxiang
Date: 2024/11/13 14:36:39
Description: FAP通用异常
"""

from faplus.utils.config_util import StatusCodeEnum


class FAPStatusCodeException(Exception):
    """FAP StatusCode通用异常类"""

    def __init__(self, code_or_enum: StatusCodeEnum | str, msg: str = None, msg_dict: dict = None) -> None:
        """
        初始化异常类

        :param code_or_enum: 异常码,或者通用异常枚举
        :param msg: 异常提示
        :param msg_dict: 异常提示占位符数据, defaults to None
        """
        if isinstance(code_or_enum, StatusCodeEnum):
            msg = code_or_enum.name
            code = code_or_enum.value
        elif isinstance(code_or_enum, str):
            assert msg, "msg is required when code is str"
            code = code_or_enum
        else:
            raise ValueError("code_or_enum must be StatusCodeEnum or str")

        if msg_dict:
            msg = msg.format(**msg_dict)

        super().__init__(msg)

        self.code = code
        self.msg = msg
