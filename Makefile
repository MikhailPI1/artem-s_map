.PHONY: help install, run migrate superuser shell docker-build docker-run docker-down

MANAGE = python manage.py

help:
	@echo "Доступные команды:"
	@echo "  install     - Установить зависимости и виртуальное окружение"
	@echo "  run         - Запустить сервер разработки"
	@echo "  migrate     - Выполнить миграции"
	@echo "  superuser   - Создать суперпользователя"
	@echo "  shell       - Открыть Django shell"
	@echo "  clean       - Очистить кэш и временные файлы"
	@echo "  docker-build - Собрать Docker образ"
	@echo "  docker-run   - Запустить в Docker"
	@echo "  docker-down  - Остановить Docker контейнеры"

install:
	python3.11 -m venv venv
	pip install -r requirements.txt

run:
	$(MANAGE) runserver

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell


docker-build:
	docker build -t artem-map .

docker-run:
	docker run -p 8000:8000 --env-file .env artem-map

docker-down:
	docker stop $$(docker ps -q --filter ancestor=artem-map) || true
