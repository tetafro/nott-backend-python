#!/bin/bash
# Entry point for production container.

LOGS_DIR=/srv/logs

touch $LOGS_DIR/gunicorn.log
touch $LOGS_DIR/access.log
touch $LOGS_DIR/django.log
tail -n 0 -f $LOGS_DIR/*.log &

echo Starting Gunicorn.
gunicorn core.wsgi:application \
    --name nott \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --log-level=info \
    --log-file=$LOGS_DIR/gunicorn.log \
    --access-logfile=$LOGS_DIR/access.log \
    "$@"
