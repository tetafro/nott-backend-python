# Install for development

1. Build images

    ```sh
    docker-compose -f docker-compose-dev.yml build
    docker-compose -f docker-compose-dev.yml run --rm app bash -c 'cd /srv/public/js/ && npm install'
    ```

2. Populate

    ```sh
    docker-compose -f docker-compose-dev.yml run --rm app python3 /srv/manage.py migrate
    docker-compose -f docker-compose-dev.yml run --rm app python3 /srv/manage.py loaddata /srv/apps/users/fixtures/admin.json
    ```

3. Run app

    ```sh
    docker-compose -f docker-compose-dev.yml up
    ```
