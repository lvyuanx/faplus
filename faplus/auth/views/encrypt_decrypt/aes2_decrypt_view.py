#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: rsa_decrypt_view.py
Author: lvyuanxiang
Date: 2024/11/15 13:50:20
Description: ASA2解密视图
"""
from fastapi import Query

from faplus.auth.encrypt.aes2 import decrypt
from faplus.utils import StatusCodeEnum
from faplus.view import PostView


class View(PostView):

    finally_code = StatusCodeEnum.AES2解密失败

    @staticmethod
    async def api(
        msg: str = Query(..., description="待解密数据"),
        key: str | None = Query(None, description="秘钥"),
    ):
        return decrypt(msg, key)
