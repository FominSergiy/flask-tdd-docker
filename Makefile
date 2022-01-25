# docker
init-build:
	docker-compose build

update-build:
	docker-compose up -d --build

run-container:
	docker-compose up

run-detached:
	docker-compose up -d

run-docker-tests:
	docker-compose exec api python -m pytest "src/tests"

run-docker-config-tests:
	docker-compose exec api python -m pytest "src/tests" -k config

run-docker-unit-tests:
	docker-compose exec api python -m pytest "src/tests" -k unit