from sud.services.cryptography.conf import ClientConfig as Config
from sud.utils import fetch, post

from aiohttp import ClientSession
import attr


@attr.s(slots=True)
class Cryptography:
    url: str = attr.ib(default=Config.url)

    async def version(self) -> str:
        return await fetch(self.url, 'version')['version']

    async def new_key(self) -> str:
        return await fetch(self.url, 'new_key', 201)['key']

    async def encrypt(self, key: str, data: str) -> str:
        result = await post(self.url, 'encrypt', dict(key=key, content=data))
        return result['data']

    async def decrypt(self, key: str, data: str) -> str:
        result = await post(self.url, 'decrypt', dict(key=key, content=data))
        return result['data']

    async def change_key(self, old_key: str, new_key: str, data: str) -> str:
        result = await post(self.url, 'change_key', dict(
            old_key=old_key,
            new_key=new_key,
            content=data
        ))
        return result['data']
