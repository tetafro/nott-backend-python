MANAGE = ./project/smart_manage.py

.PHONY: dep
dep:
	pip install -r requirements.txt

.PHONE: lint
lint:
	@ flake8 --exclude=migrations

.PHONY: test
test:
	@ $(MANAGE) test

.PHONY: migrations
migrations:
	@ $(MANAGE) makemigrations users notes

.PHONY: migrate
migrate:
	@ $(MANAGE) migrate

.PHONY: fixtures
fixtures:
	@ $(MANAGE) loaddata ./project/apps/users/fixtures/user.json

.PHONY: run
run:
	@ $(MANAGE) runserver 127.0.0.1:8080

.PHONY: docker
docker:
	@ docker build -t tetafro/nott_backend_python .
