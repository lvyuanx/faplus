#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filename: router_loader.py
Author: lvyuanxiang
Date: 2024/11/07 09:12:38
Description: 加载路由
"""
from enum import Enum
import importlib
import inspect
import logging
from types import ModuleType
from typing import Union
import uuid

from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from pydantic.main import BaseModel
from faplus.core import settings
from faplus.utils import data_util
from faplus.schema import ErrorResponseSchema
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

APPLIICATION_ROOT = settings.APPLICATION_ROOT  # 程序根app路径
FAP_DOCS_URL = settings.FAP_DOCS_URL
FAP_REDOC_URL = settings.FAP_REDOC_URL
FAP_DOC_IS_LOCAL_STATIC = settings.FAP_DOC_IS_LOCAL_STATIC
FAP_STATIC_URL = settings.FAP_STATIC_URL
FAP_STATIC_NAME = settings.FAP_STATIC_NAME
FAP_TITLE = settings.FAP_TITLE
FAP_DESCRIPTION = settings.FAP_DESCRIPTION
FAP_VERSION = settings.FAP_VERSION
FAP_CONTACT = settings.FAP_CONTACT
FAP_LICENSE = settings.FAP_LICENSE
FAP_OPENAPI_URL = settings.FAP_OPENAPI_URL
FAP_APP_DEBUG = settings.FAP_APP_DEBUG
FAP_API_CODE_NUM = settings.FAP_API_CODE_NUM
FAP_API_EXAMPLE_ADAPTER = settings.FAP_API_EXAMPLE_ADAPTER
FAP_INSERTAPPS = settings.FAP_INSERTAPPS
DEBUG = settings.DEBUG
VERSION_CONFIG = settings.FAP_VERSION_CONFIG
OPEN_DFTDAULT_VERSION = settings.FAP_OPEN_DFTDAULT_VERSION


logger = logging.getLogger(__package__)


def init_app() -> FastAPI:
    """初始化app"""
    fap_kwargs = {
        "docs_url": FAP_DOCS_URL if DEBUG else None,
        "redoc_url": FAP_REDOC_URL if DEBUG else None,
        "title": FAP_TITLE,
        "description": FAP_DESCRIPTION,
        "version": FAP_VERSION,
        "contact": FAP_CONTACT,
        "license_info": FAP_LICENSE,
        "openapi_url": FAP_OPENAPI_URL if DEBUG else None,
        "debug": FAP_APP_DEBUG if DEBUG else False,
    }
    app = FastAPI(**fap_kwargs)
    if FAP_DOC_IS_LOCAL_STATIC:
        app.docs_url = None
        app.redoc_url = None
        app.mount(
            FAP_STATIC_URL, StaticFiles(directory=FAP_STATIC_NAME), name="fap_static"
        )

        @app.get(FAP_DOCS_URL, include_in_schema=False)
        async def custom_swagger_ui_html():
            return get_swagger_ui_html(
                openapi_url=app.openapi_url,
                title=app.title + " - Swagger UI",
                oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
                swagger_js_url="/static/swagger-ui-bundle.js",
                swagger_css_url="/static/swagger-ui.css",
            )

        @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
        async def swagger_ui_redirect():
            return get_swagger_ui_oauth2_redirect_html()

        @app.get(FAP_REDOC_URL, include_in_schema=False)
        async def redoc_html():
            return get_redoc_html(
                openapi_url=app.openapi_url,
                title=app.title + " - ReDoc",
                redoc_js_url="/static/redoc.standalone.js",
            )

    return app


def generate_responses(
    api_code: str,
    status_codes: list[tuple[str, str]],
    common_codes: list[Enum],
    finally_code: Enum | tuple[str, str],
    response_model: type[BaseModel],
):
    """生成结果示例

    :param msgs: (状态码，描述)
    :return: 返回示例
    """
    if FAP_API_EXAMPLE_ADAPTER:
        adapter = importlib.import_module(FAP_API_EXAMPLE_ADAPTER)
    else:
        from ..adapters import example_adapater as adapter
    example = {}
    # success
    example[200] = {
        "description": "请求成功",
        "content": {
            "application/json": {"example": data_util.generate_example(response_model)}
        },
    }

    # error
    code_dict = {}
    for code, msg in status_codes:
        code = f"{api_code}{code}"
        example[int(code)] = {
            "description": msg,
            "content": {"application/json": {"example": adapter.error(code, msg)}},
        }
        code_dict[code] = msg
    for code_enum in common_codes:
        code, msg = code_enum.value, code_enum.name
        example[int(code)] = {
            "description": msg,
            "content": {"application/json": {"example": adapter.error(code, msg)}},
        }
        code_dict[code] = msg

    if finally_code:
        if isinstance(finally_code, Enum) and finally_code.value not in code_dict:
            code, msg = finally_code.value, finally_code.name
            example[int(code)] = {
                "description": msg,
                "content": {"application/json": {"example": adapter.error(code, msg)}},
            }

            code_dict[code] = msg

        if (
            isinstance(finally_code, tuple)
            and f"{api_code}{finally_code[0]}" not in code_dict
        ):
            code, msg = finally_code
            code = f"{api_code}{code}"
            example[int(code)] = {
                "description": msg,
                "content": {"application/json": {"example": adapter.error(code, msg)}},
            }
            code_dict[code] = msg

    return example, code_dict


def check_app(module: ModuleType):
    app_name = module.__name__.split(".views.", 1)[0]
    if app_name not in FAP_INSERTAPPS:
        raise RuntimeError(f"{app_name} app is not in FAP_INSERTAPPS")
    return app_name


def loader(app: Union[FastAPI, None] = None) -> Union[FastAPI, None]:
    api_module = f"{APPLIICATION_ROOT}.apis"

    # 加载路由配置
    apis_module = importlib.import_module(api_module)
    api_cfg = apis_module.apis

    # 初始化app
    app = init_app()

    for version_tag in VERSION_CONFIG:
        assert version_tag != "default" and version_tag != "debug", "version tag not allowed to use default or debug"

    api_group_dict = {} # key: version_tag, value: APIRouter(), APIRouter()
    for version_tag in VERSION_CONFIG.keys():
        api_group_dict[version_tag] = (APIRouter(), APIRouter())
    
    if OPEN_DFTDAULT_VERSION:
        api_group_dict["default"] = (APIRouter(), APIRouter())
    
    
    # 遍历路由组
    for gid, gurl, groups, gtag in api_cfg:
        
        # 遍历视图配置
        for pre_url, api_cfgs in groups.items():

            for api_cfg in api_cfgs:
                
                if len(api_cfg) == 4:
                    aid, aurl, amodule_or_str, aname = api_cfg
                    kwargs = {}
                else:
                    aid, aurl, amodule_or_str, aname, kwargs = api_cfg

                # 获取接口模块
                if isinstance(amodule_or_str, str):
                    api_module = importlib.import_module(amodule_or_str)
                else:
                    api_module = amodule_or_str

                check_app(api_module)

                view_endpoint = api_module.View  # 视图函数
                status_codes = view_endpoint.status_codes
                common_codes = view_endpoint.common_codes
                finally_code = view_endpoint.finally_code
                response_model = view_endpoint.response_model
                view_status = view_endpoint.view_status
                api_code = str(gid) + str(aid)
                tags = kwargs.get("tags", [])

                responses, code_dict = generate_responses(
                    api_code=api_code,
                    status_codes=status_codes,
                    common_codes=common_codes,
                    finally_code=finally_code,
                    response_model=response_model,
                )
                api_module.View.api_code = api_code
                api_module.View.code_dict = code_dict
                
                # region ******************** 遍历View中的所有方法 start ******************** #
                for name, attr in inspect.getmembers(view_endpoint, predicate=inspect.isfunction):
                    if name == "api" or hasattr(attr, "version_tag"):
                        
                        version_tag = getattr(attr, "version_tag", "default")
                        
                        # 判断api的版本设置是否正确
                        if version_tag not in VERSION_CONFIG.keys() and version_tag != "default":
                            continue
                        
                        is_debug_api = "DEBUG" in tags
                        # 视图配置
                        api_cfg = {
                            "path": gurl + pre_url + aurl,
                            "name": f"{view_status} {aname}  {api_code} {'🐞' if is_debug_api else ''} \
                                {'' if version_tag == 'default' else f'✨:{version_tag}'}",
                            "response_model": Union[view_endpoint.response_model, ErrorResponseSchema],
                            "methods": view_endpoint.methods,
                            "operation_id": f"{api_code}_{api_module.__name__}_{uuid.uuid4().hex}",
                            "responses": responses,
                        }
                        
                        api_tags = [gtag] + tags
                        if version_tag == "default":
                            group_router, debug_router = api_group_dict["default"]
                        else:
                            api_tags.append(version_tag)
                            group_router, debug_router = api_group_dict[version_tag]
                            
                        router = group_router
                        if is_debug_api:
                            router = debug_router
                            
                        router.add_api_route(
                            endpoint=attr,
                            **api_cfg,
                            tags=api_tags,
                        )
                # endregion ****************** 遍历View中的所有方法 end ********************* #    

    for version_tag, (group_router, debug_router) in api_group_dict.items():
        if version_tag == "default":
            app.include_router(router=group_router)
            app.include_router(router=debug_router, prefix="/debug")
        else:
            version_url = VERSION_CONFIG[version_tag]
            app.include_router(router=group_router, prefix=version_url)
            app.include_router(router=debug_router, prefix=f"{version_url}/debug")
    return app
