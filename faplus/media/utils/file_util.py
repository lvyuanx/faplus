#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: file_util.py
Author: lvyuanxiang
Date: 2025/01/03 16:34:47
Description: 文件操作相关工具
"""
import os
import hashlib
import logging
import secrets
import string

from fastapi import UploadFile
import aiofiles

from faplus.media.models import SNRecord

logger = logging.getLogger(__package__)


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


async def save_upload_file(
    file: UploadFile, save_path: str, file_name: str = None
) -> tuple[str, str]:
    """保存上传的文件并生成哈希值作为文件名

    :param file: 上传的文件
    :param save_path: 保存地址
    :param file_name: 文件名称（可选）
    :return: 文件的hash和文件名
    """
    if not file:
        return None

    # 创建保存目录（如果不存在的话）
    os.makedirs(save_path, exist_ok=True)

    # 获取文件内容并计算哈希值
    file_content = await file.read()
    file_hash = hashlib.sha256(file_content).hexdigest()

    # 根据是否提供自定义文件名来生成新的文件名
    final_file_name = file_name if file_name else file.filename
    hash_name = f"{file_hash}_{final_file_name}"

    file_path = os.path.join(save_path, hash_name)

    # 如果文件已经存在，跳过保存
    if os.path.exists(file_path):
        return (file_hash, final_file_name)

    # 保存文件
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(file_content)

    # 重新设置文件指针到开头
    await file.seek(0)

    return (file_hash, final_file_name)


async def delete_file(file_path: str):
    """删除文件

    :param file_path: 文件路径
    :return: 是否删除成功
    """
    if not os.path.exists(file_path):
        return
    os.remove(file_path)


async def get_file(file_path: str, file_name: str):
    """获取文件
    :param file_path: 文件路径
    :param file_name: 文件名称
    :return: 文件内容
    """
    fpath = os.path.join(file_path, file_name)
    if not os.path.exists(fpath):
        return
    async with aiofiles.open(fpath, "rb") as f:
        return await f.read()
