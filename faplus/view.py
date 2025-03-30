#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: post.py
Author: lvyuanxiang
Date: 2024/11/06 10:23:00
Description: fastapi post 视图基类
"""
import logging
import functools
from typing import Dict, Union, Callable
from enum import Enum

from fastapi import Header, Request, Body, Query, Path, Form, File, UploadFile
from fastapi.responses import Response as FAResponse
from tortoise.queryset import QuerySet

from faplus.exceptions import FAPStatusCodeException
from faplus.core import settings, StatusCodeEnum
from faplus.schema import ResponseSchema, ResponsePageSchema
from faplus.utils.api_util import Response
from .const import ViewStatusEnum

FAP_TOKEN_TAG = settings.FAP_TOKEN_TAG

logger = logging.getLogger(__package__)

import functools

def version(version_tag: str):
    """指定接口的版本
    
    版本格式：
        MAJOR.MINOR.PATCH
        当您做了不兼容的API修改时增加主版本号（MAJOR）。
        当您以向后兼容的方式添加功能时增加次版本号（MINOR）。
        当您进行向后兼容的问题修复时增加修订版本号（PATCH）。

    :param version_tag: 表示指定版本
    :return:
    """
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return version_tag, func(*args, **kwargs)
        wrapper.version_tag = version_tag # 设置版本号
        return wrapper
    return decorator


class BaseView:
    """所有视图接口的基类"""

    methods = ["POST"]  # 接口请求类型
    api_code = None  # api code码，请勿自行修改，初始化的时候，系统会自动赋值
    code_dict = {}  # 所有改接口使用到的异常码的字典，初始化的时候，系统会自动赋值

    response_model = ResponseSchema
    common_codes = []  # 通用状态码，使用
    # 最终异常码，可以使用StatusCodeEnum枚举中定义的通用状态码枚举，或者接口异常状态码(<code>, <msg>)
    finally_code = None
    status_codes = []  # 接口异常状态码(<code>, <msg>)
    view_status = ViewStatusEnum.define

    @classmethod
    def make_code(
        cls, code: Union[str, Enum], msg_dict: Dict = None
    ) -> ResponseSchema:
        if isinstance(code, str):
            code = f"{cls.api_code}{code}"
            if code not in cls.code_dict:
                raise ValueError(f"code {code} is not register")
            msg = cls.code_dict[code]
        else:
            value = code.value
            if isinstance(value, str):
                msg = code.name
                code = value
            else:
                code, msg = value
            if code not in cls.code_dict:
                raise ValueError(f"code {code} is not register")

        if msg_dict:
            msg = msg.format(**msg_dict)
        logger.warning(f"[make_code error]: {code}, msg: {msg}")
        return Response.fail(code=code, msg=msg)

    @staticmethod
    async def api():
        """抽象方法，需在子类中实现"""
        raise NotImplementedError("Subclasses should implement this method")

    @classmethod
    def _api_wrapper(cls, code: Enum | tuple[str, str] = None):
        """api装饰器，能够帮助处理异常，以及返回值的处理"""

        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                """wrapper"""
                try:
                    result = await func(*args, **kwargs)

                    # region ******************** 如果返回的是ResponseSchema直接返回 start ******************** #
                    if isinstance(result, ResponseSchema): 
                        logger.debug(f"result: {result}")
                        return result
                    # endregion ****************** 如果返回的是ResponseSchema直接返回 end ********************* #

                    # region ******************** 如果返回的是原生Response也直接返回 start ******************** #
                    if isinstance(result, FAResponse):
                        logger.debug(f"result: {result}")
                        return result
                    # endregion ****************** 如果返回的是原生Response也直接返回 end ********************* #
                    
                    # region ******************** 其他类型当OK处理 start ******************** #
                    return Response.ok(data=result)
                    # endregion ****************** 其他类型OK处理 end ********************* #
                    
                except FAPStatusCodeException as e:  # 通过异常类终止程序
                    result = Response.fail(code=e.code, msg=e.msg)
                    logger.error(f"[FAPStatusCodeException] result: {result}")
                    return result
                except Exception as e:  # 其他异常终止的程序
                    if not code:
                        raise e  # 抛出异常的话，交给异常处理中间件处理，异常打印原则：**捕获自行打印，抛出上层打印**

                    if isinstance(code, StatusCodeEnum):
                        result = Response.fail(code=code.value, msg=code.name)
                    elif isinstance(code, tuple):
                        result = cls.make_code(code=code[0])
                    else:
                        raise ValueError(
                            "code must be StatusCodeEnum or tuple(str, str)"
                        )
                    logger.error(f"[Exception] result: {result}", exc_info=True)
                    return result

            return wrapper

        return decorator

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        for name, attr in cls.__dict__.items():
            if callable(attr) and (name == "api" or hasattr(attr, "version_tag")):
                wrapped_func = cls._api_wrapper(cls.finally_code)(attr)
                setattr(cls, name, wrapped_func)


class PostView(BaseView):
    methods = ["POST"]

class PageView(BaseView):
    methods = ["POST"]

    response_model = ResponsePageSchema
    
    @classmethod
    async def paginate_query(cls, manager: QuerySet, curent_page: int = 0, page_size: int = 10, values: list[str] = None, convert = None) -> Dict:
        """分压器查询

        :param manager: 查询管理器
        :param curent_page: 当前页页码, 从0开始
        :param page_size: 当前页面大小
        :param values: 需要返回的字段列表
        :param convert: 返回数据转换函数
        :return: 返回分页数据
        """
        total = await manager.count()
        offset = curent_page * page_size
        manager = manager.offset(offset).limit(page_size)
        if values:
            manager = manager.values(*values)
        else:
            manager = manager.all()
        
        data = await manager

        if convert:
            data = [convert(item) for item in data]
        
        return {
            "curent_page": curent_page,
            "page_size": page_size,
            "total": total,
            "data": data
        }

class GetView(BaseView):
    methods = ["GET"]


class PutView(BaseView):
    methods = ["PUT"]


class DeleteView(BaseView):
    methods = ["DELETE"]


class PatchView(BaseView):
    methods = ["PATCH"]
