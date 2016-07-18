import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = ',cgi6&g]({g&9$4>g=nj:s2n3!]xh6rk{$oz#r$f|el(m|@6@n'

if os.environ.get('SERVER_MODE') == 'dev':
    DEBUG = True
else:
    DEBUG = False
    ALLOWED_HOSTS = ['nott.tk']


# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'easy_maps',
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


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_notes',
        'USER': 'pguser',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '',
    }
}


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
