#!/usr/bin/env python
"""
Backup PostreSQL database using pg_dump util. Standard env variables are used
to access the database: PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD.
Dropbox token is required to upload backup. It can be obtained here:
https://www.dropbox.com/developers/apps
"""
import time
import logging
import os
import subprocess
import sys
import tempfile
from datetime import datetime

import dropbox
import schedule


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(levelname)-8s  %(message)s')
logger = logging.getLogger()


def check():
    """Check mandatory environment variables"""

    empty = []
    mandatory_vars = ('POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_NAME',
                      'POSTGRES_PASSWORD', 'POSTGRES_USER', 'DROPBOX_TOKEN')
    for var in mandatory_vars:
        try:
            os.environ[var]
        except KeyError:
            empty.append(var)
    if empty:
        logger.error('Empty mandatory variables: %s', ', '.join(empty))
        return False

    return True


def backup():
    """Backup database to system tmp directory"""

    logger.info('Start database dump...')

    conn_str = '--dbname=postgresql://%s:%s@%s:%s/%s' % (
        os.environ['POSTGRES_USER'],
        os.environ['POSTGRES_PASSWORD'],
        os.environ['POSTGRES_HOST'],
        os.environ['POSTGRES_PORT'],
        os.environ['POSTGRES_NAME']
    )

    pg_dump = ['pg_dump', '-Fc', '-C', conn_str]
    dumpfile = os.path.join(
        tempfile.gettempdir(),
        datetime.now().strftime('%Y%m%d')+'_test.dump'
    )

    with open(dumpfile, 'w') as f:
        try:
            proc = subprocess.run(pg_dump, stdout=f)
        except FileNotFoundError:
            logger.error('pg_dump not found')
            sys.exit(1)

    if proc.returncode != 0:
        logger.error('Failed to create backup')
        return None

    logger.info('Database dump completed')
    return dumpfile


def upload(dumpfile):
    """Upload backup to Dropbox"""

    logger.info('Strat uploading backup...')

    token = os.environ.get('DROPBOX_TOKEN')
    client = dropbox.Dropbox(token)
    with open(dumpfile, 'rb') as f:
        filename = os.path.basename(dumpfile)
        try:
            client.files_upload(f.read(), '/'+filename)
        except Exception as e:
            logger.error('Upload failed with error: '+str(e))
            return False

    logger.info('Uploading backup completed')
    return True


def job():
    """Perform all steps for backup to Dropbox: check, backup, upload"""

    logger.info('Starting backup job...')

    if not check():
        return

    dumpfile = backup()
    if not dumpfile:
        return

    if not upload(dumpfile):
        return

    logger.info('Backup job completed')


schedule.every().day.at('03:00').do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
