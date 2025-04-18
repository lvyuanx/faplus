from enum import Enum


class CommonStatusCodeEnum(Enum):

    请求成功 = "0"
    请求失败 = "1"
    接口未实现 = "2"
    创建成功 = "201"
    无内容 = "204"
    永久移动 = "301"
    临时移动 = "302"
    临时重定向 = "307"
    错误请求 = "400"
    未授权 = "401"
    请求不存在 = "404"
    方法不允许 = "405"
    请求超时 = "408"
    冲突 = "409"
    有效负载过大 = "413"
    无法处理实体 = "422"
    不支持的媒体类型 = "415"
    内部服务器错误 = "500"
    网关错误 = "502"
    服务不可用 = "503"
    网关超时 = "504"
