#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: aes.py
Author: lvyuanxiang
Date: 2024/11/15 16:45:00
Description: AES加密解密,不同加密结果
"""

import os
import base64

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7

from faplus.utils import settings

FAP_AES_KEY = settings.FAP_AES_KEY


def generate_aes_key(password: str, salt: str = None) -> str:
    """
    生成一个用于 AES 加密的密钥。
    :param password: 用户提供的密码
    :param salt: 可选的盐值（如果不提供，将随机生成）
    :return: 编码的密钥
    """
    if salt is None:
        salt = os.urandom(16)
    else:
        salt = base64.b64decode(salt.encode())  # 反解码为 bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256 位密钥
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = kdf.derive(password.encode())
    return base64.b64encode(key).decode()


def encrypt(plaintext: str, key: str | None) -> str:
    """
    使用 AES 对称加密加密一个字符串。
    :param plaintext: 要加密的字符串
    :param key: base64 编码的 AES 密钥
    :return: base64 编码的加密结果（包含 IV 和加密数据）
    """
    if key is None:
        key = FAP_AES_KEY
        if key is None:
            raise ValueError("No AES key provided.")
    key = base64.b64decode(key.encode())  # 解码为 bytes
    iv = os.urandom(16)
    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    # 返回 base64 编码的加密数据（IV + 加密数据）
    return base64.b64encode(iv + encrypted).decode()


def decrypt(encrypted_text: str, key: str | None) -> str:
    """
    使用 AES 对称加密解密一个字符串。
    :param encrypted_text: base64 编码的加密字符串
    :param key: base64 编码的 AES 密钥
    :return: 解密后的原始字符串
    """
    if key is None:
        key = FAP_AES_KEY
        if key is None:
            raise ValueError("No AES key provided.")
    key = base64.b64decode(key.encode())  # 解码为 bytes
    encrypted_data = base64.b64decode(encrypted_text)
    iv = encrypted_data[:16]
    encrypted_message = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted_message) + decryptor.finalize()

    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    return decrypted.decode()
