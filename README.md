# Nott

[![CircleCI](https://circleci.com/gh/tetafro/nott.svg?style=shield)](https://circleci.com/gh/tetafro/nott)

Online notes service with markdown formatting and syntax highlight.

## Local installation

Build docker images and run the app locally
```sh
make build
make run
```

Stop
```sh
make stop
```

Teardown
```sh
make clear
```

## Deployment to the remote server

Prerequirements:

* Clean Ubuntu 16.04 or later
* SSH access using key

Build docker images and deploy new or update existing installation to the remote server
```sh
make build
make deploy
```

## Development (debug) version

Build docker images and run the app locally in debug mode

```sh
make ENV=dev build
make ENV=dev run
```

Stop
```sh
make ENV=dev stop
```

Teardown
```sh
make ENV=dev clear
```

## Working with the database

### Backup

```
docker exec nott_db_1 \
    pg_dump -U postgres -Fc -C db_nott > db_nott.dump
```

### Restore

```sh
docker exec -i nott_db_1 \
    dropdb -U postgres db_nott
docker exec -i nott_db_1 \
    createdb -U postgres db_nott
docker exec -i nott_db_1 \
    psql -U postgres db_nott -c 'GRANT ALL PRIVILEGES ON DATABASE db_nott TO pguser;'
docker exec -i nott_db_1 \
    pg_restore -U postgres -d db_nott < ./db_nott.dump
```

### Migrations

Make
```sh
make makemigrations
```

Migrate
```sh
make migrate
```
