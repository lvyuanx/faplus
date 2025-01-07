#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: models.py
Author: lvyuanxiang
Date: 2024/11/13 15:25:10
Description: 权限模块模型
"""
from tortoise import fields
from tortoise.indexes import Index
from tortoise.models import Model


class ContentType(Model):

    id = fields.IntField(pk=True, description="用户ID")
    app_label = fields.CharField(max_length=100, description="应用标签")
    model = fields.CharField(max_length=100, description="模型名称")

    class Meta:
        table = "fap_content_type"
        indexes = [
            Index(fields=["app_label", "model"], name="app_label_model_idx"),
        ]
        description = "系统模型表"
