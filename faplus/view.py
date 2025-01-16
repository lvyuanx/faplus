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
from typing import Dict, Union
from enum import Enum

from fastapi import Header, Request, Body, Query, Path, Form, File, UploadFile
from fastapi.responses import Response as FAResponse
from tortoise.queryset import QuerySet

from faplus.exceptions import FAPStatusCodeException
from faplus.utils import get_setting_with_default, StatusCodeEnum
from faplus.schema import ResponseSchema
from faplus.utils.api_util import Response
from .const import ViewStatusEnum

FAP_TOKEN_TAG = get_setting_with_default("FAP_TOKEN_TAG")

logger = logging.getLogger(__package__)


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

        # 所有api开头的方法，自动使用_api_wrapper
        for name, func in cls.__dict__.items():
            if name.startswith("api"):
                wrapped_func = cls._api_wrapper(cls.finally_code)(func)
                setattr(cls, name, wrapped_func)
    
    
    @classmethod
    async def paginate_query(cls, manager: QuerySet, curent_page: int = 0, page_size: int = 10) -> Dict:
        """分压器查询

        :param manager: 查询管理器
        :param curent_page: 当前页页码, 从0开始
        :param page_size: 当前页面大小
        """
        total = await manager.count()
        offset = curent_page * page_size
        data = await manager.offset(offset).limit(page_size).all()
        
        return {
            "curent_page": curent_page,
            "page_size": page_size,
            "total": total,
            "list": data
        }
        
         


class PostView(BaseView):
    methods = ["POST"]


class GetView(BaseView):
    methods = ["GET"]


class PutView(BaseView):
    methods = ["PUT"]


class DeleteView(BaseView):
    methods = ["DELETE"]


class PatchView(BaseView):
    methods = ["PATCH"]
