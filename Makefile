include config.env

ENV = prod
ifeq ($(ENV),dev)
compose_file = docker-compose-dev.yml
else
compose_file = docker-compose-prod.yml
endif
manage = /app/smart_manage.py

.PHONY: build
build:
	./scripts/build.sh $(ENV)

.PHONY: makemigrations
makemigrations:
	docker-compose -f $(compose_file) run --rm app $(manage) \
		makemigrations users notes admin

.PHONY: migrate
migrate:
	docker-compose -f $(compose_file) run --rm app $(manage) migrate

.PHONY: fixtures
fixtures:
	docker-compose -f $(compose_file) run --rm app $(manage) loaddata \
		/app/apps/users/fixtures/roles.json \
		/app/apps/users/fixtures/admin.json \
		/app/apps/admin/fixtures/settigs.json

.PHONE: lint
lint:
	./scripts/lint.sh

.PHONY: test
test:
	docker-compose -f $(compose_file) run \
		--rm \
		--entrypoint=python3 \
		app \
		$(manage) test

.PHONY: run
run:
	docker-compose -f $(compose_file) up

.PHONY: stop
stop:
	docker-compose -f $(compose_file) stop

.PHONY: clear
clear:
	docker-compose -f $(compose_file) down
	docker volume rm -f nott_cert nott_db nott_project

.PHONY: deploy
deploy:
	docker push tetafro/nott_web
	docker push tetafro/nott_db
	docker push tetafro/nott_app
	cd deploy/ansible && \
	ansible-playbook \
		--inventory="$(SERVER_DNS):$(SERVER_SSH_PORT)," \
		--extra-vars "domain=$(SERVER_DNS) user=$(REMOTE_USER)" \
		server-update.yml
