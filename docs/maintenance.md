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

# Update server

1. Build production version using dev image (current dir is root of the repository)

    ```sh
    docker run \
        --rm \
        --volume $(pwd):/srv \
        --workdir /srv/ \
        --tty \
        nott_app_dev \
        scripts/build.sh
    docker-compose -f docker-compose-prod.yml down
    docker-compose -f docker-compose-prod.yml build
    ```

2. Push to Docker Hub

    ```sh
    docker login
    docker push tetafro/nott_web
    docker push tetafro/nott_db
    docker push tetafro/nott_app
    docker push tetafro/nott_certbot
    ```

3. Destroy server containers and remove project volume

    ```sh
    docker-compose down
    docker volume rm nott_project
    docker rmi tetafro/nott_web tetafro/nott_db tetafro/nott_app
    ```

4. Run app again

    ```sh
    docker-compose up -d
    ```
