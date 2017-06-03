# Prepare environment for development server

1. Install Docker

2. Make network

    ```sh
    docker network create --subnet=172.20.0.0/16 docknet
    ```

3. DB server container

    ```sh
    docker volume create --name=nott-db
    docker build -t nott-db -f configs/dockerfiles/db .
    docker create \
        --name nott-db \
        --net docknet \
        --ip 172.20.0.11 \
        --volume nott-db:/var/lib/postgresql/data \
        --env POSTGRES_PASSWORD=postgres \
        nott-db
    ```

4. App container

    ```sh
    docker build -f configs/dockerfiles/app_dev -t nott-app:dev .
    docker create \
        --name nott-app \
        --net docknet \
        --ip 172.20.0.10 \
        --volume /home/tetafro/IT/projects/pet/nott/project:/srv \
        --tty \
        nott-app:dev
    ```

5. Start everything

    ```sh
    docker start nott-db
    docker start -a nott-app
    ```

6. Populate

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
