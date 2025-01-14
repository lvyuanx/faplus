#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: models.py
Author: lvyuanxiang
Date: 2024/11/13 15:25:10
Description: 权限模块模型
"""
from tortoise import fields
from tortoise.models import Model
from tortoise.indexes import Index

from faplus.utils import time_util


class SNRecord(Model):

    id = fields.IntField(pk=True, description="自增主键")
    sn = fields.CharField(unique=True, max_length=64, description="sn码")

    class Meta:
        table = "media_sn_record"
        description = "sn码表"


class FileRecord(Model):

    id = fields.IntField(pk=True, description="自增主键，用于唯一标识每个文件记录")
    original_name = fields.CharField(
        max_length=255, description="文件的真实名称，用户上传的文件名"
    )
    save_name = fields.CharField(
        max_length=255, null=True, description="文件的保存名称"
    )
    sn = fields.CharField(unique=True, max_length=64, description="文件的唯一标识")
    file_hash = fields.CharField(
        max_length=64, description="文件的哈希值（SHA256），用于唯一标识文件"
    )
    file_path = fields.CharField(max_length=512, description="文件存储在服务器上的路径")
    file_type = fields.CharField(
        max_length=255,
        description="文件类型（如：image/jpeg，application/pdf 等），根据 MIME 类型",
    )
    source = fields.CharField(
        max_length=255,
        null=True,
        description="文件的来源（如上传者、系统等），可以为空",
    )
    created_at = fields.IntField(
        default=time_util.now_timestamp(), description="文件的保存时间"
    )

    class Meta:
        table = "media_file_record"
        description = "文件记录表"

        indexes = [
            Index(fields=["file_hash"]),
        ]

    def __str__(self):
        return f"FileRecord(id={self.id}, sn={self.sn}, file_hash={self.file_hash}, file_path={self.file_path})"
