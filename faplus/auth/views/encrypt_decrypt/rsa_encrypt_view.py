#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: rsa_encrypt_view.py
Author: lvyuanxiang
Date: 2024/11/15 10:11:57
Description: RSA加密视图
"""
from fastapi import Query

from faplus.auth.encrypt.rsa import encrypt
from faplus.utils import StatusCodeEnum
from faplus.view import PostView


class View(PostView):

    finally_code = StatusCodeEnum.RSA加密失败

    @staticmethod
    async def api(
        msg: str = Query(..., description="待加密数据"),
        public_key: str | None = Query(None, description="公钥"),
    ):
        return encrypt(msg, public_key)
