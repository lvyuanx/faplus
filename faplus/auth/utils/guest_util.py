# -*-coding:utf-8 -*-

"""
# File       : guest_util.py
# Time       : 2025-01-15 15:45:53
# Author     : lyx
# version    : python 3.11
# Description: 访客工具
"""
import logging

from faplus.utils import get_setting_with_default

logger = logging.getLogger(__package__)

def generate_user_dict():
    FAP_GUEST_USERS = get_setting_with_default("FAP_GUEST_USERS")
    gest_user_dict = {}
    for user in FAP_GUEST_USERS:
        gest_user_dict[user.username] = user
    return gest_user_dict