import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VERSION = os.environ.get('VERSION') or 'Unknown'

SERVER_MODE = os.environ.get('SERVER_MODE')
if SERVER_MODE == 'production':
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    ALLOWED_HOSTS = os.environ.get('SERVER_DNS')
    if not ALLOWED_HOSTS:
        raise EnvironmentError('Allowed hosts are not set!')
    ALLOWED_HOSTS = ['localhost'] + ALLOWED_HOSTS.split(',')
elif SERVER_MODE == 'development':
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    ALLOWED_HOSTS = ['*']
else:
    raise EnvironmentError('Server mode is not set!')

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
    'widget_tweaks',
    'apps.admin',
    'apps.health',
    'apps.notes',
    'apps.users',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'core.middleware.HttpErrorsMiddleware',
)

DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')
if not DB_USER or not DB_PASS:
    raise EnvironmentError('Database credentials are not set!')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_nott',
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': 'db',
        'PORT': '5432',
    }
}

ROOT_URLCONF = 'core.urls'

AUTH_USER_MODEL = 'users.User'

# Auth URLs
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = ''

# View function to handle CSRF failures
CSRF_FAILURE_VIEW = 'core.middleware.csrf_failure'

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
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AVATARS_URL = '/media/avatars/'
AVATARS_ROOT = os.path.join(MEDIA_ROOT, 'avatars')

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
