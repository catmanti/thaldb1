from .base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa F405
    }
}

STATICFILES_DIRS = [BASE_DIR / "static"]  # noqa F405
