from .base import *  # noqa: F403


DEBUG = False

ALLOWED_HOSTS = ['64.227.187.165']

# Example PostgreSQL production database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'thaldb1',
        'USER': 'thaldbuser',
        'PASSWORD': 'pwd123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
STATIC_ROOT = BASE_DIR / "staticfiles" # noqa F405
