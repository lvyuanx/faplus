# -*-coding:utf-8 -*-

"""
# File       : file_utils.py
# Time       : 2025-01-06 22:42:24
# Author     : lyx
# version    : python 3.11
# Description: 文件操作工具
"""
import os


def copy_file(
    src_dir: str,
    dst_dir: str,
    file_names: list[str],
    replace_dict: dict[tuple[str, str]] = None,
    rename_dict: dict = None,
    replace_suffix: str = ".py",
):

    keys = replace_dict.keys() if replace_dict else []
    rename_keys = rename_dict.keys() if rename_dict else []

    for fname in file_names:

        src_file = os.path.join(src_dir, fname)
        # 目标文件,去除结尾的_template, 并添加.py后缀
        if fname in rename_keys:
            target_name = rename_dict[fname]
        else:
            target_name = fname
        dst_file = os.path.join(dst_dir, target_name[:-9] + replace_suffix)
        with open(src_file, "r", encoding="utf-8") as f:
            content = f.read()
        if replace_dict and fname in keys:
            replace_lst = replace_dict[fname]
            for k, v in replace_lst:
                content = content.replace(f"${k}$", v)
        with open(dst_file, "w", encoding="utf-8") as f:
            f.write(content)
