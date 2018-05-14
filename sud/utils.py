from aiohttp import ClientResponse
from sanic.response import json as JSONResponse
import traceback
import json
import attr


@attr.s(slots=True)
class SUDError(Exception):
    response: ClientResponse = attr.ib()

    def __str__(self):
        return 'Response(method={0}, url={1}, status={2})'.format(
            self.response.method,
            self.response.url,
            self.response.status
        )


async def handle_errors(request, exception, logger=None):
    if logger is not None:
        logger.debug(''.join(traceback.format_exception(
            type(exception),
            exception,
            exception.__traceback__
        )))

        if isinstance(exception, SUDError):
            info = await exception.response.json()
            logger.error(json.dumps(info, indent=4))

    return JSONResponse(dict(error=str(exception)), status=500)


def build_url(url, endpoint):
    return url + ('' if url.endswith('/') else '/') + endpoint


async def fetch(url, endpoint, expected=200):
    async with ClientSession() as session:
        async with session.get(build_url(url, endpoint)) as resp:
            if resp.status != expected:
                raise SUDError(resp)

            return await resp.json()


async def post(url, endpoint, expected=200, data=None):
    async with ClientSession() as session:
        async with session.post(build_url(url, endpoint), data=data) as resp:
            if resp.status != expected:
                raise SUDError(resp)

            return await resp.json()
