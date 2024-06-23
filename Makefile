DC = docker compose
APP = docker_compose/app.yaml
CONSUMER_APP = docker_compose/consumer.yaml
BOT_APP = docker_compose/bot.yaml
ENV = --env-file .env

.PHONY: consumer
consumer:
	${DC} -f ${CONSUMER_APP} ${ENV} up --build -d

.PHONY: consumer-down
consumer-down:
	${DC} -f ${CONSUMER_APP} ${ENV} down

.PHONY: consumer-logs
consumer-logs:
	${DC} -f ${CONSUMER_APP} logs -f

.PHONY: bot
bot:
	${DC} -f ${BOT_APP} ${ENV} up --build -d

.PHONY: bot-down
bot-down:
	${DC} -f ${BOT_APP} ${ENV} down

.PHONY: bot-logs
bot-logs:
	${DC} -f ${BOT_APP} logs -f
