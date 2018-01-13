import os

DEBUG = False
LOG_LEVEL = 'WARNING'

ALLOWED_HOSTS = os.environ.get('SERVER_DNS')
if not ALLOWED_HOSTS:
    raise EnvironmentError('Allowed hosts are not set!')
ALLOWED_HOSTS = ['localhost'] + ALLOWED_HOSTS.split(',')
