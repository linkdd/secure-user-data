from sud.services.app_key_store.forms import ApplicationForm, ChangeKeyForm
from sud.services.app_key_store.conf import ServerConfig as Config
from sud.services.app_key_store import __version__

from sud.services.cryptography.client import Cryptography
from sud.utils import handle_errors

from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

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
collection = db['application_keys']
crypto = Cryptography()


@app.route('/version')
async def version(request):
    return json(dict(version=__version__))


@app.route('/new_app')
async def new_app(request):
    plain_appkey = await crypto.new_key()
    appkey = await crypto.encrypt(Config.secret, plain_appkey)
    result = await collection.insert_one(dict(key=appkey))
    return json(dict(appid=str(result.inserted_id)), status=201)


@app.route('/get_key')
async def get_key(request):
    form = ApplicationForm(request.form)

    if form.validate():
        appid = ObjectId(form.data['appid'])

        document = await collection.find_one(dict(_id=appid))
        plain_appkey = await crypto.decrypt(Config.secret, document['key'])

        return json(dict(key=plain_appkey))

    else:
        return json(form.errors, status=400)


@app.route('/set_key')
async def set_key(request):
    form = ChangeKeyForm(request.form)

    if form.validate():
        appid = ObjectId(form.data['appid'])
        new_key = form.data['key']

        appkey = await crypto.encrypt(Config.secret, new_key)
        await collection.replace_one(dict(_id=appid), dict(key=appkey))

        return json(dict())

    else:
        return json(form.errors, status=400)


@app.route('/del_app')
async def del_app(request):
    form = ChangeKeyForm(request.form)

    if form.validate():
        appid = ObjectId(form.data['appid'])
        await collection.delete_one(dict(_id=appid))

        return json(dict())

    else:
        return json(form.errors, status=400)


def main():
    assert Config.secret is not None, "Missing value for APP_KEY_STORE_SECRET"

    ssl = None

    if Config.cert is not None and Config.key is not None:
        ssl = dict(cert=Config.cert, key=Config.key)

    app.run(host=Config.host, port=Config.port, ssl=ssl, debug=Config.debug)
