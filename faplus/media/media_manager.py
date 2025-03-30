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
from typing import Dict, List
from faplus.utils import settings

from fastapi import UploadFile
from .utils import file_util
from .models import FileRecord
from tortoise.transactions import in_transaction
from . import const

BASE_DIR = settings.BASE_DIR
MEDIA_ROOT = getattr(settings, "FAP_MEDIA_ROOT", os.path.join(BASE_DIR, "media"))
MEDIA_URL = settings.FAP_MEDIA_URL
FAP_TEMP_DIR = getattr(settings, "FAP_TEMP_DIR", os.path.join(MEDIA_ROOT, "temp"))

logger = logging.getLogger("media")

OpenManagerEnum = const.OpenManagerEnum

class MediaManager:
    def __init__(self, open_manager_lst: list[const.OpenManagerEnum] = None, back_dir: str = FAP_TEMP_DIR):
        """媒体管理器

        :param open_manager: 开启的管理器, 默认开启所有
        :param back_dir: 回滚的缓存文件夹, defaults to FAP_TEMP_DIR
        """
        self.sn_lst = []  # 用于存储文件的 sn
        self.open_manager_lst = open_manager_lst # 开启的管理器, 默认开启所有
        self.save_manager = None  # 保存文件的管理器
        self.delete_manager = None  # 删除文件的管理器
        self.back_dir = back_dir

    async def __aenter__(self):
        """进入 'async with' 语句时初始化资源"""
        # 初始化文件保存管理器和删除管理器
        open_manager_lst = self.open_manager_lst
        self.db_manager = in_transaction() if OpenManagerEnum.db in open_manager_lst else None 
        self.save_manager = file_util.FileSaveManager() if OpenManagerEnum.save in open_manager_lst else None 
        self.delete_manager = file_util.FileDeleteManager(self.back_dir) if OpenManagerEnum.delete in open_manager_lst else None 
        
        # 进入保存管理器和删除管理器
        if self.db_manager: await self.db_manager.__aenter__()
        if self.save_manager: await self.save_manager.__aenter__()
        if self.delete_manager: await self.delete_manager.__aenter__()
        
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出 'async with' 语句时处理回滚"""
        if self.db_manager: await self.db_manager.__aexit__(exc_type, exc_val, exc_tb)
        if self.save_manager: await self.save_manager.__aexit__(exc_type, exc_val, exc_tb)
        if self.delete_manager: await self.delete_manager.__aexit__(exc_type, exc_val, exc_tb)

    async def upload(
        self, 
        files: List[UploadFile], 
        target_dir: str = MEDIA_ROOT, 
        rename_map: Dict[int, dict] = None,
        source: str = None,
    ):
        """上传文件"""
        if not files:
            return []
        
        # 目标文件夹不存在则创建
        os.makedirs(target_dir, exist_ok=True)

        rename_map = rename_map or {}
        sn_lst = []

        try:
            for idx, file in enumerate(files):
                # 保存文件
                file_hash = await self.save_manager.save(file, target_dir)
                save_name = rename_map.get(idx)
                sn = await file_util.generate_sn()
                
                # 创建文件记录
                file_record = await FileRecord.create(
                    original_name=file.filename,
                    save_name=save_name,
                    sn=sn,
                    file_hash=file_hash,
                    file_path=target_dir,
                    file_type=file.content_type,
                    source=source,
                )
                sn_lst.append(sn)
                logger.info(f"File Upload Success -> {file_record}")
            
            self.sn_lst = sn_lst  # 保存成功的sn
        except Exception as e:
            logger.error(f"File upload failed, rolling back: {e}", exc_info=True)
            raise  # 重新抛出异常，确保事务回滚

        return sn_lst

    async def remove(self, sn_lst: List[str]):
        """根据sn删除文件和文件记录"""
        if not sn_lst:
            return []

        file_manager = FileRecord.filter(sn__in=sn_lst)
        file_data_lst = await file_manager.values("file_path", "file_hash", "sn", "original_name")
        sn_lst = []

        try:
            # 删除文件记录
            for item in file_data_lst:
                file_path = item["file_path"]
                file_hash = item["file_hash"]
                original_name = item["original_name"]
                sn = item["sn"]
                manager = FileRecord.filter(file_path=file_path, file_hash=file_hash)
                print("*"  *  100)
                print(await manager.count())
                if await manager.count() == 1: # 如果文件记录唯一，则删除文件
                    await self.delete_manager.delete(file_path, file_hash, original_name)
                await manager.filter(sn=sn).delete()
                sn_lst.append(sn)

        except Exception as e:
            logger.error(f"File removal failed, rolling back: {e}", exc_info=True)
            raise  # 重新抛出异常，确保事务回滚

        return sn_lst

    @classmethod
    async def download(cls, sn_lst: List[str]) -> tuple[bytes, str, str]:
        """下载文件"""
        file_records = await FileRecord.filter(sn__in=sn_lst)
        print(file_records)
        rst = []
        for file_record in file_records:
            file_hash = file_record.file_hash
            file_path = file_record.file_path
            original_name = file_record.original_name
            save_name = file_record.save_name
            file_type = file_record.file_type

            # 获取文件内容
            file = await file_util.get_file(file_path, file_hash, original_name)
            rst.append((file, save_name or original_name, file_type))
        
        return rst


media_upload_opens = [OpenManagerEnum.db, OpenManagerEnum.save]
media_delete_opens = [OpenManagerEnum.db, OpenManagerEnum.delete]