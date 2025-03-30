import logging
from datetime import timedelta

from starlette.responses import RedirectResponse, JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from faplus.view import PostView, Request, Response as ApiResponse
from faplus.core import settings
from faplus import const
from faplus.auth import const as auth_const
from faplus.cache import cache
from faplus.utils import time_util

logger = logging.getLogger(__package__)

FAP_TOKEN_SOURCE = settings.FAP_TOKEN_SOURCE
TokenSourceEnum = const.TokenSourceEnum


class View(PostView):

    finally_code = ("00", "登出发生异常")

    @staticmethod
    async def api(
        request: Request,
    ):
        user_id = request.state.uid
        await cache.delete(auth_const.USER_CK.format(uid=user_id))
        
        
        if FAP_TOKEN_SOURCE == TokenSourceEnum.Cookie:
            # 设置 expires 为过去的日期
            response = RedirectResponse(url=request.url.path, status_code=HTTP_401_UNAUTHORIZED)
            expires = time_util.now_timestamp() - 1
            response.set_cookie(
                key=settings.FAP_TOKEN_TAG,
                value="",
                expires=expires,
                max_age=0,
                httponly=True,
                path="/",
                secure=not settings.DEBUG  # 根据实际配置调整
            )
        
            return response