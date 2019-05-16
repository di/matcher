.state/docker-build: Dockerfile requirements/main.txt requirements/deploy.txt
	# Build our docker containers for this project.
	docker-compose build web

	# Mark the state so we don't rebuild this needlessly.
	mkdir -p .state
	touch .state/docker-build

serve: .state/docker-build
	docker-compose up --remove-orphans

wipedb:
	docker-compose run --rm web psql -h db -d postgres -U postgres -c "DROP DATABASE IF EXISTS matcher"
	docker-compose run --rm web psql -h db -d postgres -U postgres -c "CREATE DATABASE matcher ENCODING 'UTF8'"

initdb: wipedb upgradedb

migratedb:
	docker-compose run --rm web flask db migrate --message "$(MESSAGE)"

upgradedb:
	docker-compose run --rm web flask db upgrade

reformat:
	docker-compose run --rm web isort -rc matcher migrations
	docker-compose run --rm web black matcher migrations


.PHONY: default serve initdb
