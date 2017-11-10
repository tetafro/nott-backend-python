include config.env

##
# Production
##

.PHONY: build
build:
	docker-compose -f docker-compose-prod.yml build

.PHONY: run
run:
	docker-compose -f docker-compose-prod.yml up

.PHONY: stop
stop:
	docker-compose -f docker-compose-prod.yml stop

.PHONY: clear
clear:
	docker-compose -f docker-compose-prod.yml down
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

##
# Development
##

.PHONY: dev
dev-build:
	# # Install NPM packets
	docker run --rm -it -v $(CURDIR)/project/public/js:/app --entrypoint npm tetafro/webpack:8 install
	# # Build images and make containers
	docker-compose -f docker-compose-dev.yml build
	docker-compose -f docker-compose-dev.yml create
	# Prepare database
	docker-compose -f docker-compose-dev.yml run backend /srv/smart_manage.py migrate
	docker-compose -f docker-compose-dev.yml run backend /srv/smart_manage.py loaddata /srv/apps/users/fixtures/admin.json

.PHONY: dev-run
dev-run:
	docker-compose -f docker-compose-dev.yml up

.PHONY: dev-stop
dev-stop:
	docker-compose -f docker-compose-dev.yml stop

.PHONY: dev-clear
dev-clear:
	docker-compose -f docker-compose-dev.yml down
	docker volume rm nott_cert nott_db nott_project
