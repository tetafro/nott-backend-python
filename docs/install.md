# Production

Prepare server and run the app

```sh
cd deploy/ansible
ansible-playbook -K server-install.yml
```

# Development

1. Build images

    ```sh
    docker-compose -f docker-compose-dev.yml build
    docker-compose -f docker-compose-dev.yml create
    docker-compose -f docker-compose-dev.yml run --rm frontend npm install
    ```

2. Populate

    ```sh
    docker-compose -f docker-compose-dev.yml run --rm backend \
        python3 /srv/manage.py migrate
    docker-compose -f docker-compose-dev.yml run --rm backend \
        python3 /srv/manage.py loaddata /srv/apps/users/fixtures/admin.json
    ```

3. Run app

    ```sh
    docker-compose -f docker-compose-dev.yml up
    ```
