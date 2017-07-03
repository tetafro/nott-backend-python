# Production

1. [Build project](/docs/build.md)

2. Build images

    ```sh
    docker-compose -f docker-compose-prod.yml build
    ```

    or pull from Docker Hub

    ```sh
    docker pull tetafro/nott_web
    docker pull tetafro/nott_db
    docker pull tetafro/nott_app
    ```

3. Create containers

    ```sh
    docker-compose -f docker-compose-prod.yml --no-build create
    ```

3. Populate

    ```sh
    docker-compose -f docker-compose-prod.yml run --rm app \
        python3 /srv/manage.py migrate
    docker-compose -f docker-compose-prod.yml run --rm app \
        python3 /srv/manage.py loaddata /srv/apps/users/fixtures/admin.json
    ```

    or restore backup

    ```sh
    docker-compose -f docker-compose-prod.yml up
    docker exec -i nott_db_1 pg_restore -U postgres -d db_nott < ./20170624.dump
    ```

4. Run app

    ```sh
    docker-compose -f docker-compose-prod.yml up
    ```

# Dev

1. Build images

    ```sh
    docker-compose -f docker-compose-dev.yml build
    docker-compose -f docker-compose-dev.yml run --rm app \
        bash -c 'cd /srv/public/js/ && npm install'
    ```

2. Populate

    ```sh
    docker-compose -f docker-compose-dev.yml run --rm app \
        python3 /srv/manage.py migrate
    docker-compose -f docker-compose-dev.yml run --rm app \
        python3 /srv/manage.py loaddata /srv/apps/users/fixtures/admin.json
    ```

3. Run app

    ```sh
    docker-compose -f docker-compose-dev.yml up
    ```

# Build project

Build production version using dev image

```
docker run \
    --rm \
    --volume /home/tetafro/IT/projects/pet/nott:/srv \
    --workdir /srv/ \
    --tty \
    nott_dev_app \
    scripts/build.sh
```
