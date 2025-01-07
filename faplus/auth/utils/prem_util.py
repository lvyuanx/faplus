# -*-coding:utf-8 -*-

"""
# File       : prem_util.py
# Time       : 2025-01-06 21:52:57
# Author     : lyx
# version    : python 3.11
# Description: 权限工具
"""
from faplus.models import ContentType
from faplus.auth.models import Premission, Group


async def create_prem(
    app_label: str, model_name: str, name: str, codename: str
) -> Premission:
    """创建权限

    :param app_label: 应用标签
    :param model_name: 模型名称
    :param name: 权限名称
    :param codename: 权限代码
    :return: 权限实例
    """
    content_type, _ = await ContentType.get_or_create(
        app_label=app_label, model=model_name
    )

    return await Premission.get_or_create(
        name=name,
        codename=codename,
        content_type=content_type,
    )


async def create_group(name: str, premissions: list[Premission]) -> Group:
    """创建组

    :param name: 组名称
    :param premissions: 权限列表
    :return: 组实例
    """
    group, _ = await Group.get_or_create(name=name)
    group.premissions.clear()
    await group.premissions.add(*premissions)

    return group
