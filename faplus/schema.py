from pydantic import BaseModel, Field
from typing import Union


class ResponseSchema(BaseModel):
    """请求返回格式"""

    code: str = Field(description="状态码", default="0")
    msg: str | None = Field(description="状态信息")
    data: Union[dict, str] | None= Field(description="返回数据")
