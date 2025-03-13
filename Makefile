DC = docker compose
STORAGES_FILE = docker_compose/storages.yaml
APP_FILE = docker_compose/app.yaml
DB_CONTAINER = subd-db
APP_CONTAINER = main-app
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: postgres
postgres:
	${EXEC} ${DB_CONTAINER} psql

.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER}

.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER}

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash