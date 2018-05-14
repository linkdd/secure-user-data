from decouple import config


class ServerConfig:
    debug = config('DEBUG', default=False, cast=bool)
    host = config('HOST', default='0.0.0.0')
    port = config('PORT', default=8000, cast=int)
    cert = config('SSL_CERT_FILE', default=None)
    key = config('SSL_KEY_FILE', default=None)


class ClientConfig:
    url = config('CRYPTOGRAPHY_URL', default='http://127.0.0.1:8000')
