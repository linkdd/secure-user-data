from sud.services.cryptography.conf import ClientConfig as Config
from sud.utils import SUDError, post

from aiohttp import ClientSession
from typing import Tuple
import attr


@attr.s(slots=True)
class UserKeyStore:
    url: str = attr.ib(default=Config.url)

    async def version(self) -> str:
        return await fetch(self.url, 'version')['version']

    async def register(self, appid: str) -> Tuple[str, str]:
        result = await post(self.url, 'register', dict(appid=appid))
        return result['user_id'], result['user_key'], 7

    async def forget(self, appid: str, user_id: str) -> None:
        await post(self.url, 'forget', dict(appid=appid, user_id=user_id))

    async def change_key(self, appid: str) -> None:
        await post(self.url, 'change_key', dict(appid=appid))
