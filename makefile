clean:
	find . -name '*.pyc' -delete
	docker system prune

init:
	docker-compose build

test:
	docker-compose up -d postgres
	sleep 5
	-pytest
	docker-compose down

run:
	docker-compose up

stop:
	docker-compose down

check-types:
	mypy main.py api/

check-styles:
	flake8 main.py api/

run-db:
	docker-compose up -d postgres