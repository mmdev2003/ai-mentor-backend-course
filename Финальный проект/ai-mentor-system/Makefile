.PHONY: deploy build-all stop-all update-all rebuild-all
.PHONY: rebuild-app stop-app
.PHONY: rebuild-monitoring stop-monitoring
.PHONY: rebuild-db stop-db
.PHONY: set-dev-env set-prod-env set-env-to-config-template

set-dev-env:
	@export $(cat env/dev/.env env/dev/.env.app env/dev/.env.db env/dev/.env.monitoring | xargs)

set-prod-env:
	@export $(cat env/prod/.env env/prod/.env.app env/prod/.env.db env/prod/.env.monitoring | xargs)

set-env-to-config-template:
	@envsubst < ${LOKI_CONFIG_FILE}.template > ${LOKI_CONFIG_FILE}
	@envsubst < ${MONITORING_REDIS_CONFIG_FILE}.template > ${MONITORING_REDIS_CONFIG_FILE}
	@envsubst < ${TEMPO_CONFIG_FILE}.template > ${TEMPO_CONFIG_FILE}
	@envsubst < ${OTEL_COLLECTOR_CONFIG_FILE}.template > ${OTEL_COLLECTOR_CONFIG_FILE}

deploy:
	@cd ..
	@git clone git@github.com:ai-mentor-mmdev/ai-mentor-backend.git
	@git clone git@github.com:ai-mentor-mmdev/ai-mentor-frontend.git
	@cd ai-mentor-system
	@./infrastructure/nginx/install.sh
	@./infrastructure/docker/install.sh
	@mkdir -p volumes/{grafana,loki,tempo,redis,postgresql,victoria-metrics}
	@mkdir -p volumes/redis/monitoring
	@mkdir -p volumes/weed
	@mkdir -p volumes/postgresql/{backend, grafana}
	@chmod -R 777 volumes

build-all: set-env-to-config-template
	@docker compose -f ./docker-compose/db.yaml up -d --build
	sleep 20
	@docker compose -f ./docker-compose/monitoring.yaml up -d --build
	sleep 20
	@docker compose -f ./docker-compose/app.yaml up -d --build


stop-all:
	@docker compose -f ./docker-compose/apps.yaml down
	@docker compose -f ./docker-compose/monitoring.yaml down
	@docker compose -f ./docker-compose/db.yaml down

update-all:
	@git pull
	@cd ../ai-mentor-backend/ && git pull && cd ../ai-mentor-system/
	@cd ../ai-mentor-frontend/ && git pull && cd ../ai-mentor-system/

rebuild-all: update-all build-all

rebuild-app: update-all set-env-to-config-template
	@docker compose -f ./docker-compose/apps.yaml up -d --build

stop-app:
	@docker compose -f ./docker-compose/apps.yaml down

stop-monitoring:
	@docker compose -f ./docker-compose/monitoring.yaml down

stop-db:
	@docker compose -f ./docker-compose/db.yaml down

rebuild-monitoring: update-all set-env-to-config-template
	@docker compose -f ./docker-compose/monitoring.yaml down
	@docker compose -f ./docker-compose/monitoring.yaml up -d --build

rebuild-db: update-all set-env-to-config-template
	@docker compose -f ./docker-compose/db.yaml down
	@docker compose -f ./docker-compose/db.yaml up -d --build