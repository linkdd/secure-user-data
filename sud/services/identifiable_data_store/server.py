from sud.services.identifiable_data_store.conf import ServerConfig as Config
from sud.services.identifiable_data_store import __version__

from sud.utils import handle_errors

from motor.motor_asyncio import AsyncIOMotorClient

from sanic.response import json
from sanic import Sanic

from functools import partial
from logbook import Logger


logger = Logger(__name__)
app = Sanic()
app.exception(Exception)(partial(handle_errors, logger=logger))

conn = AsyncIOMotorClient(
    Config.dburl
)
db = conn.get_database()
collection = db['identifiable']


@app.route('/version')
async def version(request):
    return json(dict(version=__version__))


def main():
    ssl = None

    if Config.cert is not None and Config.key is not None:
        ssl = dict(cert=Config.cert, key=Config.key)

    app.run(host=Config.host, port=Config.port, ssl=ssl, debug=Config.debug)
