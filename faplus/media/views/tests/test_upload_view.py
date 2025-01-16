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
    ViewStatusEnum
)
from faplus.media.media_manager import MediaManager, media_upload_opens

logger = logging.getLogger(__package__)


class View(PostView):

    finally_code = ("00", "文件上传发生异常")
    view_status = ViewStatusEnum.success

    @staticmethod
    async def api(
        request: Request,
        tk: str = Header(None, description="登录token", alias=FAP_TOKEN_TAG),
        file: UploadFile = File(..., description="上传文件"),
    ):
        async with MediaManager(media_upload_opens) as manager:
            sn = await manager.upload([file])
            if not sn:  # 上传失败
                return View.make_code("00")
            else:
                return Response.ok(data=sn[0])
