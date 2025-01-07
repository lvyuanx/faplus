# -*-coding:utf-8 -*-

"""
# File       : test_download_view.py
# Time       : 2025-01-05 00:06:39
# Author     : lyx
# version    : python 3.11
# Description: 测试下载
"""
import io
import logging

import urllib.parse

from faplus.view import (
    FAP_TOKEN_TAG,
    GetView,
    Request,
    Header,
    Path,
    StatusCodeEnum,
    Response,
)
from faplus.media.media_manager import MediaManager

logger = logging.getLogger(__package__)


class View(GetView):

    finally_code = ("00", "文件下载发生异常")
    common_codes = [StatusCodeEnum.请求不存在]

    @staticmethod
    async def api(
        request: Request,
        tk: str = Header(None, description="登录token", alias=FAP_TOKEN_TAG),
        sn: str = Path(..., description="文件sn码"),
    ):
        file, _, file_type = await MediaManager.download(sn)
        if not file:
            return View.make_code(StatusCodeEnum.请求不存在)

        return Response.img(file, file_type)
