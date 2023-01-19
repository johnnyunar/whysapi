"""
Local settings for whysapi project.
Included for ease of use for purposes of this exercise.
"""
from .settings import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "whysapi",
        "USER": "whysapi",
        "PASSWORD": "whysapi",
        "HOST": "db",
        "PORT": "",
    },
    "local": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "whysapi",
        "USER": "whysapi",
        "PASSWORD": "whysapi",
        "HOST": "localhost",
        "PORT": "",
    },
    "sqlite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

STATIC_ROOT = None
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
