from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Union, Optional, Dict, List
from fastapi.exceptions import RequestValidationError



# 定义泛型类型变量，默认类型为 Union[Dict, str]
T = TypeVar("T", bound=Optional[Union[Dict, str]])


class ResponseSchema(BaseModel, Generic[T]):
    """请求返回格式"""

    code: str = Field(description="状态码", default="0")
    msg: Optional[str] = Field(description="状态信息")
    data: T = Field(description="返回数据")

class ErrorResponseSchema(BaseModel):
    """请求错误的响应"""
    code: str = Field(description="状态码", default="0")
    msg: str = Field(description="状态信息")
    
V = TypeVar("V", bound=Dict)

class PaginateSchema(BaseModel, Generic[V]):
    """分页请求返回格式"""

    curent_page: int = Field(description="当前页", default=0)
    page_size: int = Field(description="每页数量", default=10)
    total: int = Field(description="总数量", default=0)
    data: List[V] = Field(description="返回数据")


ResponsePageSchema = ResponseSchema[PaginateSchema]