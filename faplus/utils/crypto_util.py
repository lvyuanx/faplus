#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: crypto_util.py
Author: lvyuanxiang
Date: 2024/11/15 16:53:16
Description: 系统加解密工具
"""
import importlib

from faplus.core import settings

ENCRYPT_PWD = settings.FAP_ENCRYPT_PWD
COYPTO_SECURE_DATA = settings.FAP_COYPTO_SECURE_DATA

# 密码的加密
enc_pwd_module = importlib.import_module(ENCRYPT_PWD)
enc_pwd = getattr(enc_pwd_module, "encrypt")

# 铭感数据的加解密
crypto_secure_data_module = importlib.import_module(COYPTO_SECURE_DATA)
secure_encrypt = getattr(crypto_secure_data_module, "encrypt")
secure_decrypt = getattr(crypto_secure_data_module, "decrypt")


def secure_encrypt_obj(obj: list | dict, keys: list[str]):
    """加密铭感对象

    :param obj: 数组或者字典对象
    :param keys: 加密字段名称
    :return: 加密后的数据
    """
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            if k in keys:
                new_dict[k] = secure_encrypt(v)
            else:
                new_dict[k] = v
        return new_dict
    elif isinstance(obj, list):
        new_arr = []
        for data in obj:
            new_arr.append(secure_encrypt(data))
        return new_arr

    return obj


def secure_decrypt_obj(obj: dict | list, keys: list[str]) -> dict | list:
    """解密铭感对象

    :param obj: 数组或者字典对象
    :param keys: 加密字段名称
    :return: 加密后的数据
    """
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            if k in keys:
                new_dict[k] = secure_decrypt(v)
            else:
                new_dict[k] = v
        return new_dict
    elif isinstance(obj, list):
        new_list = []
        for item in obj:
            new_list.append(secure_decrypt(item))
        return new_list
    else:
        return obj
