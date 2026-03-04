from .base import *  # noqa: F403
from decouple import config, Csv

DEBUG = True

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa F405
    }
}

STATICFILES_DIRS = [BASE_DIR / "static"]  # noqa F405
