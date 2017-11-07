import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SERVER_MODE = os.environ.get('SERVER_MODE')
if SERVER_MODE == 'production':
    DEBUG = False
    LOG_LEVEL = 'WARNING'
elif SERVER_MODE == 'development':
    LOG_LEVEL = 'DEBUG'
    DEBUG = True
else:
    raise EnvironmentError('Server mode is not set!')

ALLOWED_HOSTS = os.environ.get('SERVER_DNS')
if not ALLOWED_HOSTS:
    raise EnvironmentError('Allowed hosts are not set!')
ALLOWED_HOSTS = ALLOWED_HOSTS.split(',')

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
    'apps.users',
    'apps.notes'
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
LOGIN_URL = 'apps.users.views.user_auth'
LOGOUT_URL = 'apps.users.views.user_logout'

# View function to handle CSRF failures
CSRF_FAILURE_VIEW = 'core.helpers.csrf_failure'

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
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'general',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True
        },
    }
}
