from pydantic import Field, BaseModel
from datetime import datetime

from faplus.schema import ResponseSchema


class UserSchema(BaseModel):
    """用户模型schema, 去除了冗余字段"""
    id: int
    username: str
    nickname: str | None = None
    email: str | None = None
    mobile: str | None = None
    is_superuser: bool

    class Config:
        from_attributes = True


class LoginReqSchema(BaseModel):
    """登录请求参数"""

    username: str = Field(description="用户名")
    password: str = Field(description="密码")


class _LoginResSchema(BaseModel):
    """登录响应参数"""
    token: str = Field(description="token")


class LoginResSchema(ResponseSchema):
    data: _LoginResSchema | None


class CreateUserReqSchema(BaseModel):
    """创建用户请求参数"""

    username: str = Field(description="用户名")
    password: str = Field(description="密码")
    nickname: str | None = Field(description="昵称")
    email: str | None = Field(description="邮箱")
    mobile: str | None = Field(description="手机号码")
    is_superuser: bool = Field(description="是否是超级管理员")
    is_active: bool = Field(description="是否激活")
