import os
from .base import *  # noqa # pylint: disable=unused-wildcard-import

DEBUG = False

ALLOWED_HOSTS = [os.getenv('ALLOWED_PROD_HOST', '')]
