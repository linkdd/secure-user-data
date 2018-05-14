from sud.services.user_key_store.forms import ApplicationForm, ForgetForm
from sud.services.user_key_store.conf import ServerConfig as Config
from sud.services.user_key_store import __version__

from sud.services.cryptography.client import Cryptography
from sud.services.app_key_store.client import AppKeyStore

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
crypto = Cryptography()
appstore = AppKeyStore()


@app.route('/version')
async def version(request):
    return json(dict(version=__version__))


@app.route('/register', methods=['POST'])
async def register(request):
    form = ApplicationForm(request.form)

    if form.validate():
        appid = form.data['appid']
        access_key = await appstore.get_key(appid)
        plain_user_key = await crypto.new_key()
        user_key = await crypto.encrypt(access_key, plain_user_key)

        collection = db[appid]
        result = await collection.insert_one(dict(key=user_key))

        return json(dict(
            user_id=str(result.inserted_id),
            user_key=plain_user_key
        ), status=201)

    else:
        return json(form.errors, status=400)


@app.route('/forget', methods=['POST'])
async def forget(request):
    form = ForgetForm(request.form)

    if form.validate():
        appid = form.data['appid']
        userid = ObjectId(form.data['user_id'])

        access_key = await appstore.get_key(appid)
        collection = db[appid]
        document = await collection.find_one(dict(_id=userid))
        await crypto.decrypt(access_key, document['key'])
        await collection.delete_one(dict(_id=userid))

        return json(dict())

    else:
        return json(form.errors, status=400)


@app.route('/change_key', methods=['POST'])
async def change_key(request):
    form = ApplicationForm(request.form)

    if form.validate():
        appid = form.data['appid']
        access_key = await appstore.get_key(appid)
        new_access_key = await crypto.new_key()

        collection = db[appid]

        async for document in collection.find({}):
            _id = document['_id']
            new_key = await crypto.change_key(
                access_key,
                new_access_key,
                document['key']
            )
            await collection.replace_one(dict(_id=_id), dict(key=new_key))

        appstore.set_key(appid, new_access_key)

        return json(dict())

    else:
        return json(form.errors, status=400)


def main():
    ssl = None

    if Config.cert is not None and Config.key is not None:
        ssl = dict(cert=Config.cert, key=Config.key)

    app.run(host=Config.host, port=Config.port, ssl=ssl, debug=Config.debug)
