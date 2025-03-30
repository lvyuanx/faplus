import json
import logging

from datetime import datetime
import os
from faplus.utils import settings
from faplus.utils import time_util

logger = logging.getLogger(__package__)


split_line = "#" * 30 + " FastApi Plus " + "#" * 30

logo = """
          _____                    _____                    _____                    _____            _____                    _____          
         /\    \                  /\    \                  /\    \                  /\    \          /\    \                  /\    \         
        /::\    \                /::\    \                /::\    \                /::\____\        /::\____\                /::\    \        
       /::::\    \              /::::\    \              /::::\    \              /:::/    /       /:::/    /               /::::\    \       
      /::::::\    \            /::::::\    \            /::::::\    \            /:::/    /       /:::/    /               /::::::\    \      
     /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/    /       /:::/    /               /:::/\:::\    \     
    /:::/__\:::\    \        /:::/__\:::\    \        /:::/__\:::\    \        /:::/    /       /:::/    /               /:::/__\:::\    \    
   /::::\   \:::\    \      /::::\   \:::\    \      /::::\   \:::\    \      /:::/    /       /:::/    /                \:::\   \:::\    \   
  /::::::\   \:::\    \    /::::::\   \:::\    \    /::::::\   \:::\    \    /:::/    /       /:::/    /      _____    ___\:::\   \:::\    \  
 /:::/\:::\   \:::\    \  /:::/\:::\   \:::\    \  /:::/\:::\   \:::\____\  /:::/    /       /:::/____/      /\    \  /\   \:::\   \:::\    \ 
/:::/  \:::\   \:::\____\/:::/  \:::\   \:::\____\/:::/  \:::\   \:::|    |/:::/____/       |:::|    /      /::\____\/::\   \:::\   \:::\____\ 
\::/    \:::\   \::/    /\::/    \:::\  /:::/    /\::/    \:::\  /:::|____|\:::\    \       |:::|____\     /:::/    /\:::\   \:::\   \::/    /
 \/____/ \:::\   \/____/  \/____/ \:::\/:::/    /  \/_____/\:::\/:::/    /  \:::\    \       \:::\    \   /:::/    /  \:::\   \:::\   \/____/ 
          \:::\    \               \::::::/    /            \::::::/    /    \:::\    \       \:::\    \ /:::/    /    \:::\   \:::\    \     
           \:::\____\               \::::/    /              \::::/    /      \:::\    \       \:::\    /:::/    /      \:::\   \:::\____\    
            \::/    /               /:::/    /                \::/____/        \:::\    \       \:::\__/:::/    /        \:::\  /:::/    /    
             \/____/               /:::/    /                  ~~               \:::\    \       \::::::::/    /          \:::\/:::/    /     
                                  /:::/    /                                     \:::\    \       \::::::/    /            \::::::/    /      
                                 /:::/    /                                       \:::\____\       \::::/    /              \::::/    /       
                                 \::/    /                                         \::/    /        \::/____/                \::/    /        
                                  \/____/                                           \/____/          ~~                       \/____/         
                                                                                                                                              
"""

print_template = (
    "\n\n"
    + split_line
    + """

{logo}

FastApi Plus Runserver, Version: {version}, time: {time}
{host}:{port}  reload {reload}  workers {workers}

推荐使用在线文档进行接口调试
docs: http://{host}:{port}{docs_url}

"""
    + split_line
    + "\n\n"
)


def run_info_event(**kwargs):
    async def do():
        DEBUG = settings.DEBUG
        if not DEBUG:
            return

        kwargs_str = os.environ.get("UVICORN_KWARGS")
        if not kwargs_str:
            raise Exception("UVICORN_KWARGS not found")

        kwargs = json.loads(kwargs_str)

        FAP_REDOC_URL = settings.FAP_REDOC_URL
        FAP_DOCS_URL = settings.FAP_DOCS_URL
        FAP_VERSION = settings.FAP_VERSION
        time_str = time_util.now_str()
        logger.info(
            print_template.format(
                host=kwargs["host"],
                port=kwargs["port"],
                reload=kwargs["reload"],
                workers=kwargs["workers"],
                redoc_url=FAP_REDOC_URL,
                docs_url=FAP_DOCS_URL,
                time=time_str,
                version=FAP_VERSION,
                logo=logo,
            )
        )

    return do
