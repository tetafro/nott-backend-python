#!/bin/bash
#
# Unpack the app and restart server
#

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

if [ ! -f notes.tar.gz ]; then
    echo 'Archive not found'
    exit
fi

rm -rf ./notes/
tar -xzf notes.tar.gz
cp -R notes/* /var/www/notes/project/
rm -rf ./notes/
chown -R www-data:www-data /var/www/notes/project/
service uwsgi reload

echo 'Done'