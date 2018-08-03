import os


DEBUG = os.environ.get('DEBUG') == 'true'
LOG_LEVEL = 'DEBUG' if DEBUG else 'INFO'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
if not ALLOWED_HOSTS:
    raise EnvironmentError('Allowed hosts are not set!')
ALLOWED_HOSTS = ALLOWED_HOSTS.split(',')

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise EnvironmentError('Django secret key is not set!')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
        'NAME': os.environ.get('POSTGRES_DB'),
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

# Templates are not used in this service
TEMPLATES = []

WSGI_APPLICATION = 'core.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = ''

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'general': {
            'format':
            '[%(asctime)s] [%(levelname)s] %(name)s - %(filename)s:%(lineno)s %(message)s',
            'datefmt':
            '%Y-%m-%d %H:%M:%S %z'
        },
    },
    'filters': {
        'no_healthchecks': {
            '()': 'core.log.HealthchechFilter'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'general',
            'filters': ['no_healthchecks'],
        },
    },
    'loggers': {
        'django.requests': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
        'apps': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
    }
}
