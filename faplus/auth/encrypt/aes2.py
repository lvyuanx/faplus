#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: aes2.py
Author: lvyuanxiang
Date: 2024/11/15 16:44:36
Description: AES2加密解密,相同加密结果
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

from faplus.core import settings

FAP_AES2_KEY = settings.FAP_AES2_KEY


def encrypt(data: str, key: str = None) -> str:
    """
    使用 AES 对数据进行加密，使用固定 IV 确保相同输入得到相同输出。
    :param data: 需要加密的字符串
    :param key: 加密密钥（长度必须为 16, 24 或 32 个字符）
    :return: base64 编码的加密字符串
    """
    if key is None:
        key = FAP_AES2_KEY
        if key is None:
            raise ValueError("No AES key provided.")
    # 确保密钥长度为 16, 24 或 32 个字符
    if len(key) not in [16, 24, 32]:
        raise ValueError("密钥长度必须为 16, 24 或 32 个字符")

    key_bytes = key.encode("utf-8")  # 将密钥转换为字节形式
    iv = b"\x00" * 16  # 使用固定的 16 字节 IV（全 0）
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # 对数据进行填充到 16 字节块大小
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode("utf-8")) + padder.finalize()

    # 加密并返回 base64 编码结果
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(encrypted_data).decode("utf-8")


def decrypt(encrypted_data: str, key: str = None) -> str:
    """
    使用 AES 对数据进行解密。
    :param encrypted_data: 需要解密的 base64 编码字符串
    :param key: 解密密钥（长度必须为 16, 24 或 32 个字符）
    :return: 解密后的字符串
    """
    if key is None:
        key = FAP_AES2_KEY
        if key is None:
            raise ValueError("No AES key provided.")
    if len(key) not in [16, 24, 32]:
        raise ValueError("密钥长度必须为 16, 24 或 32 个字符")

    key_bytes = key.encode("utf-8")  # 将密钥转换为字节形式
    encrypted_data = base64.b64decode(encrypted_data)
    iv = b"\x00" * 16  # 使用与加密相同的固定 IV

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # 解密数据并移除填充
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return decrypted_data.decode("utf-8")
