#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: access_token.py
Author: lvyuanxiang
Date: 2024/11/15 15:43:30
Description: 登录token构建
"""
from pydantic import BaseModel


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



class Token(BaseModel):
    access_token: str
    token_type: str
    
