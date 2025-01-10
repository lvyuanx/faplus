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
from faplus.utils import get_setting_with_default, time_util
from faplus.cache import cache


SECRET_KEY = get_setting_with_default("FAP_SECRET_KEY")
ALGORITHM = get_setting_with_default("FAP_ALGORITHM")
FAP_TOKEN_EXPIRE = get_setting_with_default("FAP_TOKEN_EXPIRE")


logger = logging.getLogger(__package__)


async def create_token(data: dict, exp_seconds: Optional[int] = None):
    to_encode = data.copy()
    if exp_seconds:
        expire = time_util.add_seconds(time_util.now(), exp_seconds)
    else:
        expire = time_util.add_seconds(time_util.now(), FAP_TOKEN_EXPIRE)
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
