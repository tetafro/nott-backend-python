# Prepare environment for development server

1. Network

    ``` bash
    docker network create --subnet=172.20.0.0/16 docknet
    ```

2. Database

    ``` bash
    docker pull postgres:9.6
    docker volume create --name=nott-db
    docker create \
        --name nott-db \
        --net docknet \
        --ip 172.20.0.11 \
        --volume nott-db:/var/lib/postgresql/data \
        --env POSTGRES_PASSWORD=postgres \
        postgres:9.6
    docker start nott-db

    docker exec -it nott-db psql -U postgres -c "CREATE ROLE pguser LOGIN PASSWORD '123';"
    docker exec -it nott-db psql -U postgres -c "CREATE DATABASE db_nott;"
    docker exec -it nott-db psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE db_nott TO pguser;"

    cat backup.sql | docker exec -i nott-db psql -U postgres db_nott
    ```

3. Application

    ``` bash
    docker pull ubuntu:16.10
    docker build -t nott .
    docker create \
        --name nott-app \
        --net docknet \
        --ip 172.20.0.10 \
        --volume /home/user/nott:/srv \
        --tty \
        nott
    docker start -a nott-app

    docker exec -it nott-app /srv/project/manage.py migrate
    ```
