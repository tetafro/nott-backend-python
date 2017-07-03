# DB backup

```
docker exec nott_db_1 \
    pg_dump -U postgres -Fc -C db_nott > db_nott.backup
```

# DB restore

```sh
docker exec -it nott_db_1 \
    dropdb -U postgres db_nott
docker exec -it nott_db_1 \
    psql -U postgres db_nott -c 'GRANT ALL PRIVILEGES ON DATABASE db_nott TO pguser;'
docker exec -it nott_db_1 \
    pg_restore -U postgres -d db_nott < ./db_nott.backup
```
