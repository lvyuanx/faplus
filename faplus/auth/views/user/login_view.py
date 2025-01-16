#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: login_view.py
Author: lvyuanxiang
Date: 2024/11/19 16:58:53
Description: 登录视图
"""
from fastapi import Body, Request

from faplus import const
from faplus.utils import StatusCodeEnum
from faplus.cache import cache
from faplus.view import PostView, ViewStatusEnum
from faplus.auth import const as auth_const
from faplus.auth.schemas import LoginReqSchema, LoginResSchema, ResponseSchema
from faplus.auth.utils import user_util
from faplus.utils import token_util

class R(ResponseSchema):
    data: LoginResSchema

class View(PostView):

    response_model = R
    finally_code = StatusCodeEnum.登录失败
    common_codes = [StatusCodeEnum.用户名或密码错误]
    view_status = ViewStatusEnum.success

    @staticmethod
    async def api(
        request: Request, data: LoginReqSchema = Body(description="登录参数")
    ):
        user_dict = await user_util.authenticate_user(data.username, data.password)
        if not user_dict:
            return View.make_code(StatusCodeEnum.用户名或密码错误)

        uid = user_dict["id"]

        # 失效之前登录的token
        otk = await cache.get(auth_const.USER_TOKEN_CK.format(uid=uid))
        if otk:
            await cache.delete(const.ACTIVATE_TOKEN_CK.format(tk=otk))

        # 创建token
        payload = {"uid": uid}
        token = await token_util.create_token(payload)

        # 重新设置token
        await cache.set(auth_const.USER_TOKEN_CK.format(uid=uid), token)

        return {"token": token, "user": user_dict}
