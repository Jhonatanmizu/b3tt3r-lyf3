DOCKER_COMPOSE = sudo docker-compose

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f

shell:
	$(DOCKER_COMPOSE) exec web uv run python manage.py shell

migrate:
	$(DOCKER_COMPOSE) exec web uv run python manage.py migrate

createsuperuser:
	$(DOCKER_COMPOSE) exec web uv run python manage.py createsuperuser

test:
	$(DOCKER_COMPOSE) exec web uv run python manage.py test