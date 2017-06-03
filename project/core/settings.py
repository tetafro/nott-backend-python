import os

server_mode = os.environ.get('SERVER_MODE')
if server_mode == 'prod':
    DEBUG = False
elif server_mode == 'dev':
    DEBUG = True
else:
    raise EnvironmentError('Server mode is not set!')

# Add either dev or production settings
if DEBUG:
    from .settings_dev import *
else:
    from .settings_prod import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


LOGFILE = os.path.join(BASE_DIR, 'logs', 'django.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': "---\n%(levelname)s %(asctime)s\nModule: %(module)s\n%(message)s"
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
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGFILE,
        },
        'file_rotate': {
            'filters': ['require_debug_false'],
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGFILE,
            'maxBytes': 1024*1024*1, # 1 MB
            'backupCount': 5,
            'formatter': 'default'
        },
    },
    'loggers': LOGGERS
}
