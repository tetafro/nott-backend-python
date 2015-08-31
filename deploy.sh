#!/bin/bash

#
# Deploying script set variables to their development or production state
# Returns 0 if no errors, 1 if errors occured
#


# Files containing vars to replace in prodaction
js_custom='./static/js/custom.js'
django_settings='./notes/settings.py'

# File with passwords (not tracked by Git)
pass_ini='./pass.ini'

# Check if all files are on their places
settings=( $js_custom $django_settings $pass_ini )
for file in "${settings[@]}"
do
    if [ ! -f $file ]
    then
        echo "Missig file: $file"
        exit 1
    fi
done

# Parse passwords file
function get_ini {
    str=$(grep -o '^'$1':.*$' $pass_ini)
    str=${str#*:}
    printf -v str "%q" $str
    echo $str
}

# Development
dev_django_csrf=$(get_ini dev_django_csrf)
dev_db_user=$(get_ini dev_db_user)
dev_db_pass=$(get_ini dev_db_pass)
# Production
pro_django_csrf=$(get_ini pro_django_csrf)
pro_db_user=$(get_ini pro_db_user)
pro_db_pass=$(get_ini pro_db_pass)


# Check input arguments and make vars replacements
if [[ $# -ne 1 || ($1 != 'pro' && $1 != 'dev') ]]
then
    echo 'Deployment script v0.1'
    echo 'Usage:'
    echo '  pro         change settings for production usage'
    echo '  dev         change settings for development usage'
    exit 1
else
    case $1 in
        # Go to production mode
        pro)
            # baseUrl in JS script
            sed -i 's/^baseUrl = '\''http:\/\/notes\.lily\.local:8080'\'';/\/\/ baseUrl = '\''http:\/\/notes\.lily\.local:8080'\'';/' $js_custom
            sed -i 's/^\/\/ baseUrl = '\''http:\/\/nott\.tk'\'';/baseUrl = '\''http:\/\/nott\.tk'\'';/' $js_custom
            # JS debug
            sed -ri 's/^(\s*)console\.log/\1\/\/ console\.log/' $js_custom
            # Debug mode in Django setting
            sed -i 's/^DEBUG = True/DEBUG = False/' $django_settings
            # Django CSRF key
            sed -i 's/^SECRET_KEY = '\''.*'\''/SECRET_KEY = '\'$pro_django_csrf\''/' $django_settings
            # DB username
            sed -i 's/^        '\''USER'\'': '\''.*'\'',/        '\''USER'\'': '\'$pro_db_user\'',/' $django_settings
            # DB password
            sed -i 's/^        '\''PASSWORD'\'': '\''.*'\'',/        '\''PASSWORD'\'': '\'$pro_db_pass\'',/' $django_settings
            # Allowed Django hosts
            sed -i 's/^ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = \['\''.nott.tk'\'', '\''.nott.tk.'\''\]/' $django_settings
            
            echo 'The app is now in production mode' ;;
        # Go to development mode
        dev)
            # baseUrl in JS script
            sed -i 's/^\/\/ baseUrl = '\''http:\/\/notes\.lily\.local:8080'\'';/baseUrl = '\''http:\/\/notes\.lily\.local:8080'\'';/' $js_custom
            sed -i 's/^baseUrl = '\''http:\/\/nott\.tk'\'';/\/\/ baseUrl = '\''http:\/\/nott\.tk'\'';/' $js_custom
            # JS debug
            sed -ri 's/^(\s*)\/\/ console\.log/\1console\.log/' $js_custom
            # Debug mode in Django setting
            sed -i 's/^DEBUG = False/DEBUG = True/' $django_settings
            # Django CSRF key
            sed -i 's/^SECRET_KEY = '\''.*'\''/SECRET_KEY = '\'$dev_django_csrf\''/' $django_settings
            # DB username
            sed -i 's/^        '\''USER'\'': '\''.*'\'',/        '\''USER'\'': '\'$dev_db_user\'',/' $django_settings
            # DB password
            sed -i 's/^        '\''PASSWORD'\'': '\''.*'\'',/        '\''PASSWORD'\'': '\'$dev_db_pass\'',/' $django_settings
            # Allowed Django hosts
            sed -i 's/^ALLOWED_HOSTS = \[.*\]/ALLOWED_HOSTS = \[\]/' $django_settings

            echo 'The app is now in development mode' ;;
    esac
    exit 0
fi