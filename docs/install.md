# Production

1. Prepare server and run the app

    ```sh
    cd deploy/ansible
    ansible-playbook -K server.yml
    ```

2. Get Let's Encrypt certificate

    ```sh
    docker exec -it nott_certbot_1 certbot certonly \
        --webroot \
        -w /srv/public/ \
        -d knott.cf \
        -d www.knott.cf
    ```

# Development

1. Build images

    ```sh
    docker-compose -f docker-compose-dev.yml build
    docker-compose -f docker-compose-dev.yml create
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
