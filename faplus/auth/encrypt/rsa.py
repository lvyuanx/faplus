#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: rsa.py
Author: lvyuanxiang
Date: 2024/11/13 16:25:14
Description: RSA加密
"""
import logging
import base64

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

from faplus.core import settings

logger = logging.getLogger("FastApiPlus-RSA")

PUBLICK_KEY = settings.FAP_PUBLICK_KEY
PRIVATE_KEY = settings.FAP_PRIVATE_KEY


def generate_key():

    # 生成 RSA 密钥对
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # 导出公钥和私钥
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # 保存公钥和私钥到文件
    with open("private_key.pem", "wb") as f:
        f.write(private_pem)

    with open("public_key.pem", "wb") as f:
        f.write(public_pem)

    logger.info("Private Key:", private_pem.decode())
    logger.info("Public Key:", public_pem.decode())


# 使用公钥加密数据
def encrypt(data: str, public_key: str | None = None):
    if public_key is None:
        public_key = PUBLICK_KEY
    pub_key_obj = serialization.load_pem_public_key(public_key.encode())
    encrypted_data = pub_key_obj.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return base64.b64encode(encrypted_data).decode("utf-8")


def decrypt(encrypted_data: str, private_key: str | None):
    if not private_key:
        private_key = PRIVATE_KEY
    # 加载私钥
    private_key_obj = serialization.load_pem_private_key(
        private_key.encode(), password=None, backend=default_backend()
    )

    # 解密数据
    encrypted_data_bytes = base64.b64decode(encrypted_data)  # 从 base64 解码成字节
    decrypted_data = private_key_obj.decrypt(
        encrypted_data_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return decrypted_data.decode("utf-8")
