import os
from .base import *  # noqa # pylint: disable=unused-wildcard-import


DEBUG = True

ALLOWED_HOSTS = ['*','127.0.0.1', '0.0.0.0', os.getenv('ALLOWED_LOCAL_HOST', '')]

CORS_ORIGIN_WHITELIST = [
    'http://134.209.28.109:8088',
    'http://localhost:3000',
    'https://localhost:3000',
    'http://127.0.0.1:3000',
    'https://127.0.0.1:3000',
    'https://127.0.0.1:8088',
    ]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
