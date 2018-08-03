MANAGE = ./project/smart_manage.py

.PHONY: dep
dep:
	pip install -r requirements.txt

.PHONE: lint
lint:
	@ flake8 ./project

.PHONY: test
test:
	@ $(MANAGE) test ./project

.PHONY: migrations
migrations:
	@ $(MANAGE) makemigrations users notes

.PHONY: migrate
migrate:
	@ $(MANAGE) migrate

.PHONY: run
run:
	@ $(MANAGE) runserver 127.0.0.1:8080

.PHONY: docker
docker:
	@ docker build -t tetafro/nott-backend-python .
