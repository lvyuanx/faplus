#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: media_manager.py
Author: lvyuanxiang
Date: 2025/01/03 17:11:15
Description: 媒体管理
"""
import logging
import os
from faplus.utils import get_setting_with_default

from fastapi import UploadFile
from .utils import file_util
from .models import FileRecord

BASE_DIR = get_setting_with_default("BASE_DIR")
MEDIA_ROOT = get_setting_with_default("FAP_MEDIA_ROOT", os.path.join(BASE_DIR, "media"))
MEDIA_URL = get_setting_with_default("FAP_MEDIA_URL")

logger = logging.getLogger(__package__)


class MediaManager:

    @classmethod
    async def upload(
        cls, file: UploadFile, file_path: str = None, source: str = None
    ) -> str | None:
        """上传文件

        :param file: 上传的文件
        :param file_path: 文件路径, 会拼接上MEDIA_ROOT（可选）
        :param file_name: 文件名称（可选）
        :return: 文件sn码
        """
        if file_path:
            file_path = os.path.join(MEDIA_ROOT, file_path)
        else:
            file_path = MEDIA_ROOT

        file_type = file.content_type

        try:

            # 保存文件
            file_hash, file_name = await file_util.save_upload_file(file, file_path)

            # 生成sn码
            sn = await file_util.generate_sn()

            await FileRecord.create(
                original_name=file_name,
                file_hash=file_hash,
                file_type=file_type,
                file_path=file_path,
                sn=sn,
                source=source,
            )
            return sn
        except Exception as e:
            logger.error("upload file error", exc_info=e)

    @classmethod
    async def download(cls, sn: str) -> tuple[bytes, str, str]:
        """下载文件

        :param sn: 文件sn
        :return: 文件路径和文件名,文件类型
        """

        file_record = await FileRecord.filter(sn=sn).first()
        file_hash = file_record.file_hash
        file_path = file_record.file_path
        file_name = file_record.original_name
        file_type = file_record.file_type

        file = await file_util.get_file(file_path, f"{file_hash}_{file_name}")
        return file, file_name, file_type
