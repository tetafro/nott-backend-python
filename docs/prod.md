# Install for production

1. Clone repository

2. Install Docker

3. [Build project](/docs/build.md)

4. Build images and run

    ```sh
    docker-compose build
    docker-compose up -d
    ```

5. Populate (while running)

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
