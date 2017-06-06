# Install for development

1. Clone repository

2. Install Docker

3. Make network

    ```sh
    docker network create --subnet=172.20.0.0/16 docknet
    ```

4. DB server container

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

5. App container

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

6. Start everything

    ```sh
    docker start nott-db
    docker start -a nott-app
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
