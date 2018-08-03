#!/usr/bin/env python
"""
Custom manage script that waits for DB to come up and only then runs
command as a standard manage script.
"""

import os
import sys
import time
import psycopg2
from django.core.management import execute_from_command_line
from core import settings


# Time in seconds to wait between DB checks
WAIT_TIME = 3
# Number of failed DB checks before exit
RETRIES = 10


def pgtest(host, name, user, passwd):
    """Test if PostgreSQL database is available"""
    try:
        conn = psycopg2.connect(
            "host='%s' dbname='%s' user='%s' password='%s' connect_timeout=1" %
            (host, name, user, passwd)
        )
        conn.close()
        return True
    except:
        return False


def run_command():
    """Ping default database and run command if it's ready"""

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    db_settings = (
        settings.DATABASES['default']['HOST'],
        settings.DATABASES['default']['NAME'],
        settings.DATABASES['default']['USER'],
        settings.DATABASES['default']['PASSWORD']
    )

    tries = 0
    db_ready = pgtest(*db_settings)
    while not db_ready and tries < RETRIES:
        print('Waiting for the database...')
        time.sleep(WAIT_TIME)
        tries += 1
        db_ready = pgtest(*db_settings)

    if db_ready:
        execute_from_command_line(sys.argv)
    else:
        print('Database is not responding')


if __name__ == '__main__':
    run_command()
