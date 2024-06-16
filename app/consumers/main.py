from faststream import FastStream
from faststream.kafka.broker import KafkaBroker

from consumers.handlers import router
from settings import get_settings


settings = get_settings()
broker = KafkaBroker(settings.KAFKA_BROKER_URL)
broker.include_router(router=router)
app = FastStream(broker=broker)
