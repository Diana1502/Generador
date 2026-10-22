from .base import *

DEBUG = False

ALLOWED_HOSTS = ['10.4.8.8', 'localhost', '127.0.0.1']

STATIC_ROOT = BASE_DIR / 'staticfiles'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detallado': {
            'format': '{levelname} | {asctime} | Modulo: {module} | {message}',
            'style': '{',
        },
    },
    'handlers': {
        'archivo': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django_eventos.log',
            'formatter': 'detallado',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['archivo'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
