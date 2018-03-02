import os


SERVER_MODE = os.environ.get('SERVER_MODE')
if SERVER_MODE == 'production':
    from .settings_prod import DEBUG, LOG_LEVEL, ALLOWED_HOSTS
elif SERVER_MODE == 'development':
    from .settings_dev import DEBUG, LOG_LEVEL, ALLOWED_HOSTS
else:
    raise EnvironmentError('Server mode is not set!')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Version
TAG = os.environ.get('TAG')
BUILD = os.environ.get('BUILD')

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise EnvironmentError('Django secret key is not set!')

# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.admin',
    'apps.base',
    'apps.files',
    'apps.health',
    'apps.notes',
    'apps.users',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'core.middleware.DisableCSRFForAPI',
    'core.middleware.AuthAPI',
)

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'core.backends.TokenBackend',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}
for key, value in DATABASES['default'].items():
    if not value:
        raise EnvironmentError('Database setting is empty: %s' % key)

ROOT_URLCONF = 'core.urls'

AUTH_USER_MODEL = 'users.User'

# Auth URLs
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = ''

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.add_debug',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = '/public/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'public'),
)
STATIC_ROOT = ''

# User uploads
MEDIA_URL = STATIC_URL + 'media/'
MEDIA_ROOT = os.path.join(STATICFILES_DIRS[0], 'media')

# Length of the longest avatar size in pixels
AVATAR_SIZE = 180

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'general': {
            'format': '[%(asctime)s] [%(levelname)s] '
                      '%(name)s - %(filename)s:%(lineno)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S %z'
        },
        'request': {
            'format': '[%(asctime)s] [%(levelname)s] '
                      '%(name)s - %(filename)s:%(lineno)s %(message)s '
                      'STATUS: %(status_code)s '
                      'REQUEST: %(request)s '
                      'EXCEPTION: %(exc_info)s',
            'datefmt': '%Y-%m-%d %H:%M:%S %z'
        },
        'db': {
            'format': '[%(asctime)s] [%(levelname)s] '
                      '%(name)s - %(filename)s:%(lineno)s %(message)s '
                      'DURATION: %(duration)s '
                      'SQL: %(sql)s '
                      'PARAMS: %(params)s '
                      'EXCEPTION: %(exc_info)s)',
            'datefmt': '%Y-%m-%d %H:%M:%S %z'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'django': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'general',
        },
        'request': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'request',
        },
        'db': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'db',
        },
        'apps': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'general',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'django.request': {
            'handlers': ['request'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'django.db.backends': {
            'handlers': ['db'],
            'level': 'ERROR',
            'propagate': False,
        },
        'apps': {
            'handlers': ['apps'],
            'level': LOG_LEVEL,
        },
    }
}
