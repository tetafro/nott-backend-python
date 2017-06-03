"""Prod-only settings"""

ALLOWED_HOSTS = ['nott.tk']

SECRET_KEY = ',cgi6&g]({g&9$4>g=nj:s2n3!]xh6rk{$oz#r$f|el(m|@6@n'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_nott',
        'USER': 'pguser',
        'PASSWORD': '123',
        'HOST': '172.20.0.11',
        'PORT': '5432',
    }
}

LOGGERS = {
    'django.request': {
        'handlers': ['file'],
        'level': 'WARNING',
        'propagate': True
    },
}