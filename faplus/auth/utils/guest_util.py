# -*-coding:utf-8 -*-

"""
# File       : guest_util.py
# Time       : 2025-01-15 15:45:53
# Author     : lyx
# version    : python 3.11
# Description: 访客工具
"""
import logging

from faplus.core import settings

logger = logging.getLogger(__package__)

def generate_user_dict():
    FAP_GUEST_USERS = settings.FAP_GUEST_USERS
    gest_user_dict = {}
    for user in FAP_GUEST_USERS:
        gest_user_dict[user.username] = user
    return gest_user_dict