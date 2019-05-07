.state/docker-build: Dockerfile requirements/main.txt requirements/deploy.txt
	# Build our docker containers for this project.
	docker-compose build web

	# Mark the state so we don't rebuild this needlessly.
	mkdir -p .state
	touch .state/docker-build

serve: .state/docker-build
	docker-compose up --remove-orphans

initdb:
	docker-compose run --rm web psql -h db -d postgres -U postgres -c "DROP DATABASE IF EXISTS matcher"
	docker-compose run --rm web psql -h db -d postgres -U postgres -c "CREATE DATABASE matcher ENCODING 'UTF8'"
	docker-compose run --rm web python -m alembic upgrade head



.PHONY: default serve initdb
