include config.env

compose_file = docker-compose-prod.yml

.PHONY: build
build:
	docker-compose -f $(compose_file) build

.PHONY: run
run:
	docker-compose -f $(compose_file) up

.PHONY: stop
stop:
	docker-compose -f $(compose_file) stop

.PHONY: clear
clear:
	docker-compose -f $(compose_file) down
	docker volume rm nott_cert nott_db nott_project

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
