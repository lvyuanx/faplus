from enum import IntEnum, StrEnum

ACTIVATE_TOKEN_CK = "activate_token:{tk}"
WHITELIST_CK = "whitelist:{url}"
STATIC_CK = "static:{url}"


class TokenSourceEnum(IntEnum):
    """Token获取的来源"""
    
    Header = 1 # 请求头
    Query = 2   # 请求参数
    Body = 3    # 请求体
    Cookie = 4  # Cookie
    
    
class ViewStatusEnum(StrEnum):
    """视图状态枚举"""
    
    define = "📝" 
    develop = "🔨" 
    test = "🧪"
    success = "✅"
    
