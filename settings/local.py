from .base import *

DEBUG = True

# Credentials for superuser created via `manage.py create_dev_superuser`
DEV_SUPERUSER_EMAIL = 'admin@admin.com'
DEV_SUPERUSER_PASSWORD = 'admin123'






# Mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Uncomment and set settings below
# EMAIL_HOST =
# EMAIL_PORT =
# EMAIL_HOST_USER =
# EMAIL_HOST_PASSWORD =

DEFAULT_FROM_EMAIL = 'vdrive_postmaster@atomcream.com'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}