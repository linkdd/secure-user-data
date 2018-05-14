from sud.services.app_key_store.conf import ClientConfig as Config
from sud.utils import SUDError, fetch, post

from aiohttp import ClientSession
from typing import Tuple
import attr


@attr.s(slots=True)
class AppKeyStore:
    url: str = attr.ib(default=Config.url)

    async def version(self) -> str:
        return await fetch(self.url, 'version')['version']

    async def new_app(self) -> str:
        return await fetch(self.url, 'new_app', 201)['appid']

    async def get_key(self, appid: str) -> str:
        return await post(self.url, 'get_key', dict(appid=appid))['key']

    async def set_key(self, appid: str, key: str) -> None:
        await post(self.url, 'set_key', dict(appid=appid, key=key))

    async def del_app(self, appid: str) -> None:
        await post(self.url, 'del_app', dict(appid=appid))
