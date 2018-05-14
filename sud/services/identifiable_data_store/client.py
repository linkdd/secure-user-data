from sud.services.identifiable_data_store.conf import ClientConfig as Config
from sud.utils import fetch, post

from aiohttp import ClientSession
from typing import Dict, Any
import attr


@attr.s(slots=True)
class IdentifiableDataStore:
    url: str = attr.ib(default=Config.url)

    async def version(self) -> str:
        return await fetch(self.url, 'version')['version']

    async def register(self, appid: str, user_data: Dict[str, Any]) -> str:
        pass

    async def get_profile(self, appid: str, user_id: str) -> Dict[str, Any]:
        pass

    async def update_profile(
        self,
        appid: str,
        user_id: str,
        user_data: Dict[str, Any]
    ) -> None:
        pass

    async def forget(self, appid: str, user_id: str) -> None:
        pass
