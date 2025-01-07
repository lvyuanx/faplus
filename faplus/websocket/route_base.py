import importlib
import json
import logging

from fastapi import WebSocket
from fastapi.routing import APIWebSocketRoute


logger = logging.getLogger(__package__)

class RouteBase(APIWebSocketRoute):

    url = "" # 路由地址
    user_class = "" # 用户类（需要继承 UserBase）
        
    
    async def endpoint(self, websocket: WebSocket):
        path, name = self.user_class.rsplit(".", 1) 
        user_module = importlib.import_module(path)
        user = getattr(user_module, name)
        await user().run(websocket)

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, path=self.url, endpoint=self.endpoint, **kwargs)