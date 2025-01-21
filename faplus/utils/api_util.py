import io
import urllib.parse
from typing import Any

from fastapi.responses import StreamingResponse, Response as FAResponse
from faplus.utils.config_util import StatusCodeEnum
from faplus.schema import ResponseSchema


class Response(object):
    @staticmethod
    def ok(msg: str = None, data: dict | str = None) -> ResponseSchema:
        """返回正常响应

        :param msg: 消息, defaults to None
        :param data: 响应的数据, defaults to None
        :return: ResponseSchema
        """
        return ResponseSchema(code=StatusCodeEnum.请求成功, msg=msg, data=data)

    @staticmethod
    def fail(code: str, msg: str, data: Any = None):
        return ResponseSchema(code=code, msg=msg, data=data)

    @staticmethod
    def download(file: bytes, file_name: str = None):
        # 文件名可能是非ASCII字符，所以我们需要正确地编码它。
        encoded_filename = urllib.parse.quote(file_name)
         # 设置 Content-Disposition 头
        content_disposition = f"attachment; filename={encoded_filename}"

        return StreamingResponse(
            io.BytesIO(file),
            media_type="application/octet-stream",
            headers={"Content-Disposition": content_disposition},
        )

    @staticmethod
    def img(file: bytes, content_type: str):
        return FAResponse(content=file, media_type=content_type)
