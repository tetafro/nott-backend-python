"""Dev-only settings"""

ALLOWED_HOSTS = []

LOGGERS = {
    'django.request': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True
    }
}
