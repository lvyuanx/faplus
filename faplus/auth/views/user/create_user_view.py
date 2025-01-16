#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: create_user_view.py
Author: lvyuanxiang
Date: 2024/11/21 09:43:28
Description: 开发环境创建用户
"""
from fastapi import Body, Request

from faplus.utils import StatusCodeEnum
from faplus.view import PostView, ViewStatusEnum
from faplus.auth.schemas import CreateUserReqSchema
from faplus.auth.utils import user_util


class View(PostView):

    finally_code = StatusCodeEnum.用户创建失败
    view_status = ViewStatusEnum.success

    @staticmethod
    async def api(
        request: Request, data: CreateUserReqSchema = Body(description="用户数据")
    ):
        """
        创建用户

        **注意**：该接口仅仅用于测试环境快速生成用户，生产环境请自行编写用户创建方法
        """
        await user_util.create_user(**data.dict())
