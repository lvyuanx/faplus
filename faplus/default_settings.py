#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: default_settings.py
Author: lvyuanxiang
Date: 2024/11/19 17:23:40
Description: FAP用到的所有默认配置
"""
from pathlib import Path

DEBUG = True
BASE_DIR = Path(__file__).resolve().parent.parent

# 在线文档swagger地址
FAP_DOCS_URL = "/docs"

# 在线文档redoc地址
FAP_REDOC_URL = "/redoc"

# 是否使用本地静态文件
FAP_DOC_IS_LOCAL_STATIC = False

# 静态文件地址前缀
FAP_STATIC_URL = "/static"

# 静态文件目录
FAP_STATIC_NAME = "static"

# 文档标题
FAP_TITLE = "FAP ONLINE DOCS"

# 文档说明
FAP_DESCRIPTION = ""

# 文档版本
FAP_VERSION = "0.0.1"

# 开启的版本
OPEN_VERSION = [""]

# 联系方式
FAP_CONTACT = {}

# 许可证
FAP_LICENSE = {}

# openapi接口地址
FAP_OPENAPI_URL = "/openapi.json"

# FastApi是否开启debug
FAP_APP_DEBUG = False

# api码位数
FAP_API_CODE_NUM = 2

# 文档中示例的适配器
FAP_API_EXAMPLE_ADAPTER = None

# 注册的app模块
FAP_INSERTAPPS = []

# AES加密解密(加密结果不同)
FAP_AES_KEY = None

# AES加密解密(加密结果相同)
FAP_AES2_KEY = None

# RSA公钥
FAP_PUBLICK_KEY = None

# RSA私钥
FAP_PRIVATE_KEY = None

# 密码加密
FAP_ENCRYPT_PWD = "faplus.auth.encrypt.md5"

# 铭感数据加密
FAP_COYPTO_SECURE_DATA = "faplus.auth.encrypt.aes2"

# 程序密钥
FAP_SECRET_KEY = None

# tk加密算法
FAP_ALGORITHM = "HS256"

# 访问令牌过期时间
FAP_ACCESS_TOKEN_EXP = 30

# jwt白名单
FAP_JWT_WHITES = []

# 登录地址
FAP_LOGIN_URL = "/user/login"

# token标记
FAP_TOKEN_TAG = "X-Authorization"

# 开机自启的模块
FAP_STARTUP_FUNCS = []

# 关机自动触发的模块
FAP_SHUTDOWN_FUNCS = []

# 中间件
FAP_MIDDLEWARE_CLASSES = []


# 数据库相关
DB_USERNAME = "root"
DB_PASSWORD = "123456"
DB_HOST = "localhost"
DB_PORT = 3306
DB_DATABASE = None
DB_ENGINE = None
DB_CHARSET = "utf8mb4"
DB_TIMEZONE = "Asia/Shanghai"
DB_MAXSIZE = 20
DB_MINSIZE = 1
DB_GENERATE_SCHEMAS = False
DB_INSERTAPPS = []
DB_DEBUG = True

# 日志相关
PROJECT_APP_PACKAGES = []
LOG_LEVEL = "DEBUG"
LOG_DIR = "logs"
LOGGING = None

# 缓存相关
FAP_CACHE_CONFIG = {
    "default": {
        "BACKEND": "faplus.cache.backends.menory_cache.MemoryCache",
    }
}

# websocket 路由
FAP_WS_CLASSES = []

FAP_TOKEN_EXPIRE = 60 * 60 * 24 * 7  # token过期时间
FAP_CACHE_DEFAULT_EXPIRE = 60 * 60 * 24 * 7  # 默认缓存过期时间

# 媒体
FAP_MEDIA_DIR = None
FAP_MEDIA_URL = "/media"
