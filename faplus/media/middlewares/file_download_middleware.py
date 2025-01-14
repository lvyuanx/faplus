# -*-coding:utf-8 -*-

"""
# File       : file_download_middleware.py
# Time       : 2025-01-05 15:35:15
# Author     : lyx
# version    : python 3.11
# Description: 文件下载中间件
"""

import logging

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from faplus.utils import get_setting_with_default, Response as ApiResponse, StatusCodeEnum
from faplus.media import MediaManager

logger = logging.getLogger(__package__)

MEDIA_URL = get_setting_with_default("FAP_MEDIA_URL")


class FileDownloadMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # 获取url
        path = request.url.path
        print(path)
        if not path.startswith(MEDIA_URL):
            return await call_next(request)

        # 获取文件的sn（url的最后一截）
        sn = path.split("/")[-1]

        rst = await MediaManager.download([sn])
        if not rst:
            return Response(
                ApiResponse.fail(StatusCodeEnum.请求不存在.value, StatusCodeEnum.请求不存在.name).json(),
                headers={"Content-Type": "application/json"},
            )
        
        file, file_name, file_type = rst[0]
        if file_type.startswith("image"):
            return ApiResponse.img(file, file_type)
        else:
            return ApiResponse.download(file, file_name)
