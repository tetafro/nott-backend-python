#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    # Dev server runs manage.py directly and uses settings_dev. Production uses
    # core/settings.py (it's in the core/wsgi.py)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_dev')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
