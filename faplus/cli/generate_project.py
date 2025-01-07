# -*-coding:utf-8 -*-

"""
# File       : init_project.py
# Time       : 2025-01-06 22:55:10
# Author     : lyx
# version    : python 3.11
# Description: 初始化项目
"""
import os
from .utils import file_util
from pathlib import Path

current_path = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_path, "templates")


def startproject(root_dir: str, root_app: str):
    root_app_files = [
        "__init___template",
        "apis_template",
        "http_status_code_template",
        "models_template",
        "settings_template",
    ]

    replace_dict = {"settings_template": [("APPLICATION_ROOT", root_app)]}

    root_app_path = os.path.join(root_dir, root_app)

    # 创建根目录
    os.makedirs(root_app_path, exist_ok=True)

    file_util.copy_file(
        src_dir=template_dir,
        dst_dir=root_app_path,
        replace_dict=replace_dict,
        file_names=root_app_files,
    )

    file_util.copy_file(
        src_dir=template_dir,
        dst_dir=root_dir,
        file_names=["config_template", "manage_template"],
        replace_dict={"manage_template": [("root_app", root_app)]},
    )

    file_util.copy_file(
        src_dir=template_dir,
        dst_dir=root_dir,
        file_names=["requirements_template"],
        replace_suffix=".txt",
    )


def startapp(app_dir: str, app_name: str):

    app_path = os.path.join(app_dir, app_name)
    os.makedirs(app_path, exist_ok=True)
    view_dir = os.path.join(app_path, "views")
    os.makedirs(view_dir, exist_ok=True)

    file_util.copy_file(
        src_dir=template_dir,
        dst_dir=view_dir,
        file_names=["__init___template"],
    )

    app_files = [
        "__init___template",
        "apis_app_template",
        "models_template",
        "schemas_template",
    ]

    rename_dict = {"apis_app_template": "apis_template"}

    file_util.copy_file(
        src_dir=template_dir,
        dst_dir=app_path,
        file_names=app_files,
        rename_dict=rename_dict,
    )


if __name__ == "__main__":
    print(current_path)
