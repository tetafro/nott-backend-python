# Nott

[![CircleCI](https://circleci.com/gh/tetafro/nott-backend-python.svg?style=shield)](https://circleci.com/gh/tetafro/nott-backend-python)

Online notes service with markdown formatting and syntax highlight.

This repository provides backend written in python.

## Build and run

Define database creds
```sh
export PGUSER=postgres
export PGPASSWORD=postgres
export PGDATABASE=nott
```

Run PostgreSQL
```sh
docker run -d \
    --name postgres \
    --publish 127.0.0.1:5432:5432 \
    --env "POSTGRES_USER=${PGUSER}" \
    --env "POSTGRES_PASSWORD=${PGPASSWORD}" \
    --env "POSTGRES_DB=${PGDATABASE}" \
    postgres:10
```

Create and populate config
```sh
cp .env.example .env
source .env
```

Build and run the application
```sh
make dep migrate run
```
