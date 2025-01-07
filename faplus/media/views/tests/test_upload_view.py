# -*-coding:utf-8 -*-

"""
# File       : test_upload_view.py
# Time       : 2025-01-04 22:46:25
# Author     : lyx
# version    : python 3.11
# Description: 测试上传文件
"""
import logging

from faplus.view import (
    FAP_TOKEN_TAG,
    PostView,
    Request,
    Header,
    UploadFile,
    File,
    Response,
)
from faplus.media.media_manager import MediaManager

logger = logging.getLogger(__package__)


class View(PostView):

    finally_code = ("00", "文件上传发生异常")

    @staticmethod
    async def api(
        request: Request,
        tk: str = Header(None, description="登录token", alias=FAP_TOKEN_TAG),
        file: UploadFile = File(..., description="上传文件"),
    ):
        sn = await MediaManager.upload(file)
        if not sn:  # 上传失败
            return View.make_code("00")
        else:
            return Response.ok(data=sn)
