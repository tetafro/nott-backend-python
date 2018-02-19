#!/bin/bash

env=$1

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/..
webpack_image=tetafro/webpack:8
manage=/app/smart_manage.py

case $env
    'prod')
        docker-compose -f $dir/docker-compose-prod.yml build
    ;;
    'dev')
        # Install NPM packets
        docker run --rm -it \
            -v $dir/project/public/js:/app \
            --entrypoint npm \
            $webpack_image \
            install
        # Build images and make containers
        docker-compose -f $dir/docker-compose-dev.yml build
        docker-compose -f $dir/docker-compose-dev.yml up --no-start
        # Prepare database
        docker-compose -f $dir/docker-compose-dev.yml run --rm backend $manage migrate
        docker-compose -f $dir/docker-compose-dev.yml run --rm backend $manage loaddata \
            /app/apps/users/fixtures/roles.json \
            /app/apps/users/fixtures/admin.json \
            /app/apps/admin/fixtures/settings.json
    ;;
    *)
        echo "Invalid environment: '$env'"
        exit 1
    ;;
esac
