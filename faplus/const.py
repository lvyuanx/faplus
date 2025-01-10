from enum import Enum

ACTIVATE_TOKEN_CK = "activate_token:{tk}"
WHITELIST_CK = "whitelist:{url}"
STATIC_CK = "static:{url}"


class TokenSourceEnum(Enum):
    """Token获取的来源"""
    
    Header = 1 # 请求头
    Query = 2   # 请求参数
    Body = 3    # 请求体
    Cookie = 4  # Cookie
    