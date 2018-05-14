from sud.services.cryptography.forms import EncryptionForm, KeyChangeForm
from sud.services.cryptography.conf import ServerConfig as Config
from sud.services.cryptography import __version__
from sud.utils import handle_errors

from sanic.response import json
from sanic import Sanic

from cryptography.fernet import Fernet, MultiFernet
from logbook import Logger
from functools import partial


logger = Logger(__name__)
app = Sanic(__name__)
app.exception(Exception)(partial(handle_errors, logger=logger))


@app.route('/version')
async def version(request):
    return json(dict(version=__version__))


@app.route('/new_key', methods=['POST'])
async def new_key(request):
    return json(dict(
        key=await app.loop.run_in_executor(
            None,
            lambda: Fernet.generate_key().decode('utf-8')
        )
    ), status=201)


@app.route('/encrypt', methods=['POST'])
async def encrypt(request):
    form = EncryptionForm(request.form)

    if form.validate():
        key = Fernet(form.data['key'].encode('utf-8'))
        data = form.data['content'].encode('utf-8')

        encrypted = await app.loop.run_in_executor(
            None,
            partial(key.encrypt, data)

        )

        return json(dict(data=encrypted.decode('utf-8')))

    else:
        return json(form.errors, status=400)


@app.route('/decrypt', methods=['POST'])
async def decrypt(request):
    form = EncryptionForm(request.form)

    if form.validate():
        key = Fernet(form.data['key'].encode('utf-8'))
        data = form.data['content'].encode('utf-8')

        decrypted = await app.loop.run_in_executor(
            None,
            partial(key.decrypt, data)
        )

        return json(dict(data=decrypted.decode('utf-8')))

    else:
        return json(form.errors, status=400)


@app.route('/change_key', methods=['POST'])
async def change_key(request):
    form = KeyChangeForm(request.form)

    if form.validate():
        old_key = Fernet(form.data['old_key'].encode('utf-8'))
        new_key = Fernet(form.data['new_key'].encode('utf-8'))
        data = form.data['content'].encode('utf-8')

        keys = MultiFernet([new_key, old_key])

        recrypted = await app.loop.run_in_executor(
            None,
            partial(keys.rotate, data)
        )

        return json(dict(data=recrypted.decode('utf-8')))

    else:
        return json(form.errors, status=400)


def main():
    ssl = None

    if Config.cert is not None and Config.key is not None:
        ssl = dict(cert=Config.cert, key=Config.key)

    app.run(host=Config.host, port=Config.port, ssl=ssl, debug=Config.debug)
