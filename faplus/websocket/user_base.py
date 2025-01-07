
import json
import logging
from fastapi import WebSocket, WebSocketDisconnect


logger = logging.getLogger(__package__)

class UserBase:

    def __init__(self):
        self.user = None
    
    
    def _load_data(self, msg: str):
        try:
            body = json.loads(msg)
            return body["code"], body["data"]
        except json.JSONDecodeError:
            logger.error("[{user}] Invalid JSON msg: {msg}".format(user=self.user, msg=msg), exc_info=True)
        except Exception:
            logger.error("[{user}] ws load data error".format(user=self.user), exc_info=True)
        
        return None, None
        
    async def join(self, websocket: WebSocket):
        await websocket.accept()
    
    async def exit(self, websocket: WebSocket):
        pass
    
    async def run(self, websocket: WebSocket):
        await self.join(websocket)
        logger.info("[{user}] websocket connected".format(user=self.user))
        try:
            while True:
                msg = await websocket.receive_text()
                logger.debug("[{user}] Received message : {msg}".format(user=self.user, msg=msg))
                code, data = self._load_data(msg)
                if not code or not data:
                    continue
                
                # 根据消息获取处理函数
                code_func = getattr(self, f"handle_{code}", None)
                if not code_func:
                    logger.warn("[{user}]code: {code} not found".format(user=self.user, code=code))
                    continue
                try:
                    await code_func(websocket, data)
                except Exception:
                    logger.error("ws func code_%s error", code, exc_info=True)
                
        except WebSocketDisconnect as e:
            logger.info("[{user}] websocket closed".format(user=self.user))
            await self.exit(websocket)