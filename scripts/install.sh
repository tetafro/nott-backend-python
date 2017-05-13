#!/bin/bash
#
# Unpack the app and restart server
#

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit
fi

if [ ! -f nott.tar.gz ]; then
    echo 'Archive not found'
    exit
fi

rm -rf ./nott/
tar -xzf nott.tar.gz
cp -R nott/* /var/www/nott/project/
rm -rf ./nott/
chown -R www-data:www-data /var/www/nott/project/
service uwsgi reload

echo 'Done'