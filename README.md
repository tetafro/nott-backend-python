# Description

Online notes service.

# Tech Stack

* Python 3
* Django
* PostgreSQL
* BackboneJS
* Twitter Bootstrap

# Installation

Build docker images and run the app locally

```sh
make build
make run
```

Stop
```sh
make stop
```

Teardown
```sh
make down
```

# Deployment

Prerequirements:

* Clean Ubuntu 16.04 or later
* SSH access using key

Deploy:

1. Set server's SSH address:port in `deploy/ansible/hosts`.

2. Set server's DNS name and remote user name in  `deploy/ansible/vars.yml`.

3. Run the deploy

    ```sh
    make deploy
    ```

# Development (debug) version

Build docker images and run the app locally in debug mode

```sh
make dev-build
make dev-run
```

Teardown
```sh
make down
```
