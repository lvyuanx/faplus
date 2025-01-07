import logging

from faplus.cache import cache
logger = logging.getLogger(__package__)


def create_startup_event(**kwargs):
    async def pring_caches():
        for cache_obj in cache.all_backend():
            await cache_obj.ping()
    return pring_caches
