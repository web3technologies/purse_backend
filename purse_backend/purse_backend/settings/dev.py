from purse_backend.settings.settings import *


CORS_ORIGIN_ALLOW_ALL = True

DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000'
]