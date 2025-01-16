#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: rsa_decrypt_view.py
Author: lvyuanxiang
Date: 2024/11/15 13:50:20
Description: RSA解密视图
"""
from fastapi import Query, Request

from faplus.auth.encrypt.rsa import decrypt
from faplus.utils import StatusCodeEnum
from faplus.view import PostView, ViewStatusEnum


class View(PostView):

    finally_code = StatusCodeEnum.RSA解密失败
    view_status = ViewStatusEnum.success

    @staticmethod
    async def api(
        msg: str = Query(..., description="待解密数据"),
        private_key: str | None = Query(None, description="私钥"),
    ):
        return decrypt(msg, private_key)
