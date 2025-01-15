#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: file_util.py
Author: lvyuanxiang
Date: 2025/01/03 16:34:47
Description: 文件操作相关工具, 只用于文件操作，不记录数据库
"""
import os
import hashlib
import logging
import secrets
import string
import asyncio
import shutil

from fastapi import UploadFile
import aiofiles

from faplus.media.models import SNRecord


logger = logging.getLogger("media")


async def generate_sn(len: int = 18, retry: int = 0) -> str:
    """生成唯一的指定长度的sn码（包含字母数字）

    :param len: sn码长度, 最低长度为16位
    :return: sn码
    """
    if retry > 5:
        logger.error("生成sn码失败，重试次数过多")
        raise Exception("生成sn码失败")
    len = max(16, len)

    # 定义字符集：包括大小写字母和数字
    characters = string.ascii_letters + string.digits

    # 使用 secrets.choice 从字符集中随机选择字符以构建 SN 码
    sn = "".join(secrets.choice(characters) for _ in range(len))

    if await SNRecord.exists(sn=sn):  # 如果生成的 SN 码已经存在，则重新生成
        return await generate_sn(len, retry + 1)
    else:
        # 占用sn
        await SNRecord.create(sn=sn)

    return sn
        

class FileSaveManager:
    def __init__(self):
        self.save_files = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.error(
                f"Failed to save files. Rolling back changes. Files=[{','.join(self.save_files)}]",
                exc_info=True,
            )
            await self.rollback()

    async def rollback(self):
        tasks = []
        for file in self.save_files:
            tasks.append(self._remove_file(file))
        await asyncio.gather(*tasks)

    async def _remove_file(self, file: str):
        try:
            await asyncio.to_thread(os.remove, file)
            logger.debug(f"Rolled back file successfully: {file}")
        except Exception as e:
            logger.error(f"Error rolling back file: {file}.", exc_info=True)

    async def save(self, file: UploadFile, target_dir: str) -> str:
        if not file:
            raise ValueError("No file provided")

        # 判断目标文件夹是否存在，不存在则创建
        os.makedirs(target_dir, exist_ok=True)

        # 计算Hash，判断文件是否重复
        content = await file.read()
        original_name = file.filename
        file_hash = hashlib.sha256(content).hexdigest()
        target_path = os.path.join(target_dir, f"{file_hash}_{original_name}")

        if not os.path.exists(target_path):
            # 保存文件
            async with aiofiles.open(target_path, "wb") as f:
                await f.write(content)
            self.save_files.append(target_path)
            logger.info(f"File saved successfully: {target_path}")
        else:
            logger.info(f"File already exists: {target_path}")

        # 重置指针
        await file.seek(0)

        return file_hash


class FileDeleteManager:
    def __init__(self, backup_dir: str):
        """
        初始化文件删除管理器。

        :param backup_dir: 用于存储备份文件的目录路径
        """
        self.deleted_files = []  # 记录原始文件路径和对应的备份文件路径
        self.backup_dir = os.path.abspath(backup_dir)  # 备份文件存储目录
        os.makedirs(self.backup_dir, exist_ok=True)  # 确保备份目录存在

    async def __aenter__(self):
        self.deleted_files = []
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            logger.error(
                f"发生异常，开始回滚已删除的文件: {self.deleted_files}",
                exc_info=True,
            )
            await self.rollback()

    async def delete(self, file_path: str):
        """
        删除文件并备份以便回滚。

        :param file_path: 需要删除的文件路径
        """
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在，跳过删除: {file_path}")
            return

        try:
            # 备份文件到备份目录
            backup_path = os.path.join(self.backup_dir, os.path.basename(file_path))
            await asyncio.to_thread(shutil.copy, file_path, backup_path)

            # 删除文件
            await asyncio.to_thread(os.remove, file_path)
            self.deleted_files.append((file_path, backup_path))
            logger.info(f"文件已删除并备份: {file_path} -> {backup_path}")
        except Exception as e:
            logger.error(f"删除文件失败: {file_path}. 错误: {e}", exc_info=True)
            raise

    async def rollback(self):
        """
        恢复所有已删除并备份的文件。
        """
        remaining_backups = []  # 记录未回滚成功的备份文件
        for file_path, backup_path in self.deleted_files:
            try:
                await self._restore_file(file_path, backup_path)
                # 回滚成功后删除备份文件
                await self._delete_backup_file(backup_path)
            except Exception as e:
                logger.error(f"回滚文件失败: {file_path}. 错误: {e}", exc_info=True)
                remaining_backups.append((file_path, backup_path))

        if remaining_backups:
            logger.warning("以下文件未能回滚，请管理员手动检查备份文件:")
            for file_path, backup_path in remaining_backups:
                logger.warning(f"原路径: {file_path}, 备份路径: {backup_path}")

    async def _restore_file(self, file_path: str, backup_path: str):
        """
        从备份目录恢复文件。

        :param file_path: 原始文件路径
        :param backup_path: 备份文件路径
        """
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"备份文件不存在: {backup_path}")
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            await asyncio.to_thread(shutil.copy, backup_path, file_path)
            logger.info(f"文件已恢复: {file_path}")
        except Exception as e:
            logger.error(f"恢复文件失败: {file_path}. 错误: {e}", exc_info=True)
            raise

    async def _delete_backup_file(self, backup_path: str):
        """
        删除单个备份文件。

        :param backup_path: 备份文件路径
        """
        try:
            if os.path.exists(backup_path):
                await asyncio.to_thread(os.remove, backup_path)
                logger.info(f"备份文件已删除: {backup_path}")
        except Exception as e:
            logger.error(f"删除备份文件失败: {backup_path}. 错误: {e}", exc_info=True)


async def get_file(dir_path: str, file_hash: str, original_name: str):
    """
    获取文件内容。

    :param dir_path: 文件所在目录路径
    :param file_hash: 文件的哈希值，用作文件名
    :param original_name: 文件的原始名称
    :return: 文件内容（字节串）或 None 如果文件不存在
    """
    file_path = os.path.join(dir_path, f"{file_hash}_{original_name}")

    # 检查文件是否存在
    if not os.path.exists(file_path):
        return None

    # 读取文件内容
    try:
        async with aiofiles.open(file_path, "rb") as f:  # 以二进制模式读取
            return await f.read()
    except Exception as e:
        # 捕获并记录读取文件时的异常
        logger.error(f"读取文件失败: {file_path}, 错误: {e}", exc_info=True)
        return None
