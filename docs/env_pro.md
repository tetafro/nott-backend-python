# Prepare environment for production server

1. Install Docker

2. Build project

    ```sh
    ./scripts/build.sh
    ```

3. Make network

    ```sh
    docker network create --subnet=172.20.0.0/16 docknet
    ```

4. Make volumes

    ```sh
    docker volume create --name=nott-db
    docker volume create --name=nott-media
    ```

5. Build images

    ```sh
    docker build -t nott-db -f configs/dockerfiles/db .
    docker build -t nott-web -f configs/dockerfiles/web .
    docker build -t nott-app:prod -f configs/dockerfiles/app_prod .
    ```

6. Create containers

    ```sh
    docker create \
        --name nott-db \
        --net docknet \
        --ip 172.20.0.11 \
        --volume nott-db:/var/lib/postgresql/data \
        --env POSTGRES_PASSWORD=postgres \
        nott-db
    docker create \
        --name nott-app \
        --net docknet \
        --ip 172.20.0.10 \
        nott-app:prod
    docker create \
        --name nott-web \
        --net docknet \
        --ip 172.20.0.12 \
        --volumes-from nott-app \
        nott-web
    ```

7. Start containers

    ```sh
    docker start nott-db
    docker start nott-web
    docker start nott-app
    ```

8. Populate

    ```sh
    docker exec \
        --tty \
        --interactive \
        nott_app_1 \
        python3 /srv/manage.py migrate
    docker exec \
        --tty \
        --interactive \
        nott_app_1 \
        python3 /srv/manage.py loaddata /srv/apps/users/fixtures/admin.json
    ```
