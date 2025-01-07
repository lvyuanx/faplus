#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: token_util.py
Author: lvyuanxiang
Date: 2024/11/15 17:20:09
Description: token工具
"""
import logging
from typing import Optional
from datetime import datetime, timedelta

import jwt  # PyJWT库

from faplus import const
from faplus.utils import get_setting_with_default
from faplus.cache import cache


SECRET_KEY = get_setting_with_default("FAP_SECRET_KEY")
ALGORITHM = get_setting_with_default("FAP_ALGORITHM")
ACCESS_TOKEN_EXP = get_setting_with_default("FAP_ACCESS_TOKEN_EXP")


logger = logging.getLogger(__package__)


async def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXP)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    await cache.set(const.ACTIVATE_TOKEN_CK.format(tk=encoded_jwt), "1")
    return encoded_jwt


async def verify_token(token: str | None) -> dict | None:
    if not token:
        return
    if not await cache.get(const.ACTIVATE_TOKEN_CK.format(tk=token)):  # token 失效了
        return
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        logger.error("", exc_info=True)
        return
