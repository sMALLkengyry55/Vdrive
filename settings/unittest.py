from .testing import *  # noqa

ALLOWED_HOSTS = []

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
