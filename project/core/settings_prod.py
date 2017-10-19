"""Prod-only settings"""

ALLOWED_HOSTS = ['nott.tk', 'knott.cf', 'nott.doc']

LOGGERS = {
    'django.request': {
        'handlers': ['file'],
        'level': 'WARNING',
        'propagate': True
    },
}
