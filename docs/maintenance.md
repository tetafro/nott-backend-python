# DB backup

```
docker exec nott_db_1 \
    pg_dump -U postgres -Fc -C db_nott > db_nott.dump
```

# DB restore

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

# Migrations

Make:
```sh
docker-compose -f docker-compose-dev.yml run --rm backend \
    python3 /srv/manage.py makemigrations
```

Migrate:
```sh
docker-compose -f docker-compose-dev.yml run --rm backend \
    python3 /srv/manage.py migrate
```

# Update server

Build production images and update the server using Ansible

```sh
make build
make deploy
    ```
