# -*-coding:utf-8 -*-

"""
# File       : config_util2.py
# Time       : 2025-03-29 23:23:56
# Author     : lyx
# version    : python 3.11
# Description: FAP 配置读取工具
"""
import logging
import importlib
import os

logger = logging.getLogger(__package__)


class ConfigLoader:

    def __init__(
            self, 
            settings_module: str = "settings", 
            default_settings: str = "faplus.default_settings", 
            config_module: str = "config"
        ):
        self.config_module_name = config_module
        self.config_module = None  # 初始化为 None
        self.settings_module_name = settings_module
        self.settings_module = None  # 初始化为 None
        self.default_settings_module_name = default_settings
        self.default_settings_module = None
        self.merge_dict = {}
        self.reload()
    
    def _load_config(self):
        try:
            self.config_module = importlib.import_module(self.config_module_name)
        except ImportError:
            self.config_module = None
            logger.warning(f"config module {self.config_module_name} not found, use default config")
        try:
            self.settings_module = importlib.import_module(self.settings_module_name)
        except ImportError:
            self.settings_module = None
            logger.warning(f"settings module {self.settings_module_name} not found, use default config")
        try:
            self.default_settings_module = importlib.import_module(self.default_settings_module_name)
        except ImportError:
            self.default_settings_module = None
            logger.warning(f"default settings module {self.default_settings_module_name} not found, use default config")
    
    def reload(self):
        self.config_module = None
        self.settings_module = None
        self.default_settings_module = None
        self.merge_dict = {}
        self._load_config()
        
    def __getattr__(self, name):
        if name in self.merge_dict:
            return self.merge_dict[name]
        # 检查 config_module 是否存在
        if self.config_module is not None and hasattr(self.config_module, name):
            value = getattr(self.config_module, name)
            self.merge_dict[name] = value
            return value
        # 检查 settings_module 是否存在
        if self.settings_module is not None and hasattr(self.settings_module, name):
            value = getattr(self.settings_module, name)
            self.merge_dict[name] = value
            return value
        # 检查 default_settings_module 是否存在
        if self.default_settings_module is not None and hasattr(self.default_settings_module, name):
            value = getattr(self.default_settings_module, name)
            self.merge_dict[name] = value
            return value
        raise AttributeError(f"'settings' or 'config' object has no attribute '{name}'")


FAP_SETTINGS_MODULE = os.environ.get("FAP_SETTINGS_MODULE")
FAP_CONFIG_MODULE = os.environ.get("FAP_CONFIG_MODULE", "config")

settings = ConfigLoader(
    settings_module=FAP_SETTINGS_MODULE,
    config_module=FAP_CONFIG_MODULE
)


def import_status_code_enum():
    try:
        # 确保 settings.APPLIICATION_ROOT 是可信的
        application_root = settings.APPLICATION_ROOT
        if not application_root:
            raise ValueError("settings.APPLICATION_ROOT is not set or is empty")

        # 动态导入模块
        module_path = f"{application_root}.http_status_code"
        module = importlib.import_module(module_path)

        # 获取 StatusCodeEnum
        status_code_enum = getattr(module, "StatusCodeEnum", None)
        if status_code_enum is None:
            raise AttributeError(
                f"Module {module_path} does not contain 'StatusCodeEnum'"
            )

        return status_code_enum
    except (ImportError, AttributeError, ValueError) as e:
        raise RuntimeError(f"Failed to import StatusCodeEnum: {e}") from e


StatusCodeEnum = import_status_code_enum()