#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: rsa_encrypt_view.py
Author: lvyuanxiang
Date: 2024/11/15 10:11:57
Description: MD5加密视图
"""
from fastapi import Query

from faplus.auth.encrypt.md5 import encrypt
from faplus.utils import StatusCodeEnum
from faplus.view import PostView, ViewStatusEnum


class View(PostView):

    finally_code = StatusCodeEnum.MD5加密失败
    view_status = ViewStatusEnum.success

    @staticmethod
    async def api(msg: str = Query(..., description="待加密数据")):
        return encrypt(msg)
