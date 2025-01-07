from typing import Union

from fastapi import FastAPI
from ..logging import init_logging


def loader(app: Union[FastAPI, None] = None) -> Union[FastAPI, None]:
    init_logging()
    return app
