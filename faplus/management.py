# -*-coding:utf-8 -*-

"""
# File       : management.py
# Time       : 2025-01-07 09:20:33
# Author     : lyx
# version    : python 3.11
# Description: faplus 管理入口
"""

import argparse
import os


class Management:

    def get_args(self):
        """获取命令行参数"""
        parser = argparse.ArgumentParser(description="FastApiPlus 启动参数")
        # 创建子解析器，用于管理子命令
        subparsers = parser.add_subparsers(dest="command", help="子命令")

        # runserver
        parser_runserver = subparsers.add_parser("runserver", help="启动服务器")
        parser_runserver.add_argument(
            "--host_port",
            type=str,
            default="127.0.0.1:8848",
            help="指定服务器监听的 host 和 port，格式如 127.0.0.1:8000",
        )
        parser_runserver.add_argument(
            "--reload", action="store_true", help="是否开启热加载模式"
        )
        parser_runserver.add_argument(
            "--workers", type=int, default=1, help="指定工作进程数"
        )

        # makemigrations
        subparsers.add_parser("makemigrations", help="生成数据库迁移文件")

        # init db
        subparsers.add_parser("init_db", help="初始化数据库")

        # migrate
        subparsers.add_parser("migrate", help="执行数据库迁移")

        # history
        subparsers.add_parser("history", help="查看数据库迁移历史")

        # downgrade
        parser_downgrade = subparsers.add_parser("downgrade", help="回滚数据库迁移")
        parser_downgrade.add_argument("--version", type=str, help="回滚版本")

        # 创建初始化项目
        parser_startproject = subparsers.add_parser("startproject", help="创建项目")
        parser_startproject.add_argument(
            "--name", type=str, default="main", help="项目名"
        )

        # 创建初始化app
        parser_startapp = subparsers.add_parser("startapp", help="创建app")
        parser_startapp.add_argument("--name", type=str, default="main", help="app名")

        args = parser.parse_args()

        self.command_args = args

        return args

    def execute(self):
        command_dict = {
            "runserver": self.runserver,
            "makemigrations": self.makemigrations,
            "init_db": self.init_db,
            "migrate": self.migrate,
            "downgrade": self.downgrade,
            "history": self.history,
            "startproject": self.startproject,
            "startapp": self.startapp,
        }
        self.get_args()
        command = self.command_args.command
        command_dict[command]()

    def _execute_command(self, cmd: str):
        import subprocess

        subprocess.run(cmd, shell=True)

    # region ******************** command func start ******************** #
    def runserver(self):
        """启动服务器"""
        import uvicorn
        import json
        from faplus.utils import get_setting_with_default

        host, port = self.command_args.host_port.split(":")

        uvicorn_kwargs = {
            "app": "faplus.applications:app",
            "host": host,
            "port": int(port),
            "reload": self.command_args.reload,
            "workers": self.command_args.workers,
            "log_level": "debug",
            "log_config": get_setting_with_default("LOGGING")
            
        }

        os.environ.setdefault("UVICORN_KWARGS", json.dumps(uvicorn_kwargs))
        uvicorn.run(**uvicorn_kwargs)

    def makemigrations(self):
        """生成数据库迁移文件"""
        self._execute_command("aerich migrate")

    def init_db(self):
        """初始化数据库"""
        self._execute_command(f"aerich init -t {__package__}.orm.tortoise.TORTOISE_ORM")
        self._execute_command("aerich init-db")

    def migrate(self):
        """执行数据库迁移"""
        self._execute_command("aerich upgrade")

    def downgrade(self):
        """回滚数据库迁移"""
        version = self.command_args.version
        self._execute_command(f"aerich downgrade -v {version} -d")

    def history(self):
        """查看数据库迁移历史"""
        self._execute_command("aerich downgrade --help")

    def startproject(self):
        """创建项目"""
        from faplus.cli import generate_project

        generate_project.startproject(os.getcwd(), self.command_args.name)

    def startapp(self):
        """创建app"""
        from faplus.cli import generate_project

        generate_project.startapp(os.getcwd(), self.command_args.name)

    # endregion ****************** command func end ********************* #


def execute_from_command_line():
    Management().execute()


if __name__ == "__main__":
    execute_from_command_line()
