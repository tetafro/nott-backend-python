# Prepare environment for production server

1. Install Docker

2. Make network

    ```sh
    docker network create --subnet=172.20.0.0/16 docknet
    ```

3. Make volumes

    ```sh
    docker volume create --name=nott-db
    docker volume create --name=nott-media
    ```

4. Build images

    ```sh
    docker build -t nott-db -f configs/dockerfiles/db .
    docker build -t nott-web -f configs/dockerfiles/web .
    docker build -t nott-app:prod -f configs/dockerfiles/app_prod .
    ```

3. Create containers

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

6. Start containers

    ```sh
    docker start nott-db
    docker start nott-web
    docker start nott-app
    ```

7. Populate

    ```sh
    docker exec \
        --tty \
        --interactive \
        nott-app \
        python3 /srv/manage.py migrate
    docker exec \
        --tty \
        --interactive \
        nott-app \
        python3 /srv/manage.py loaddata /srv/apps/users/fixtures/admin.json
    ```
