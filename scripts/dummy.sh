#!/bin/bash
#
# Switch to "under construction" dummy
#

# Config file
pro_config='/etc/nginx/sites-available/notes'
dummy_config='/etc/nginx/sites-available/dummy'

# Check if all files are on their places
required_files=( $pro_config $dummy_config )
for file in "${required_files[@]}"
do
    if [ ! -f $file ]
    then
        echo "Missig file: $file"
        exit 1
    fi
done

# Check input arguments and replace configs
if [[ $# -ne 1 || ($1 != 'dummy' && $1 != 'pro') ]]
then
    echo 'Dummy script v0.1'
    echo 'Usage:'
    echo '  pro         switch to production site'
    echo '  dummy       switch to dummy'
    exit 1
else
    case $1 in
        # Switch to production site
        pro)
            rm -f /etc/nginx/sites-enabled/dummy
            ln -s /etc/nginx/sites-available/notes /etc/nginx/sites-enabled/
            service nginx reload

            echo 'The site is now in production mode' ;;
        # Switch to dummy
        dummy)
            rm -f /etc/nginx/sites-enabled/notes
            ln -s /etc/nginx/sites-available/dummy /etc/nginx/sites-enabled/
            service nginx reload

            echo 'The site now is dummy' ;;
    esac
fi

exit 0
