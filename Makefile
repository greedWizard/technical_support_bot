DC = docker compose
APP = docker_compose/app.yaml
CONSUMER_APP = docker_compose/consumer.yaml
ENV = --env-file .env

.PHONY: consumer
consumer:
	${DC} -f ${CONSUMER_APP} ${ENV} up --build -d

.PHONY: consumer-logs
consumer-logs:
	${DC} -f ${CONSUMER_APP} logs -f
