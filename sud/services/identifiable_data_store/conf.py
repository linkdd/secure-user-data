from decouple import config


class ServerConfig:
    debug = config('DEBUG', default=False, cast=bool)
    host = config('HOST', default='0.0.0.0')
    port = config('PORT', default=8003, cast=int)
    cert = config('SSL_CERT_FILE', default=None)
    key = config('SSL_KEY_FILE', default=None)
    dburl = config(
        'DATABASE_URL',
        default='mongodb://localhost:27017/identifiable-data-store'
    )


class ClientConfig:
    url = config(
        'CIDENTIFIABLE_DATA_STORE_URL',
        default='http://127.0.0.1:8003'
    )
