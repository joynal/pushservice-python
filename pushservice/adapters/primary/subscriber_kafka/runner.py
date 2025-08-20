import logging
from collections.abc import Callable

from kafka import KafkaConsumer
from pushservice.adapters.primary.runnable import Runnable
from pushservice.settings import KafkaSettings
from pushservice.settings import WorkerSettings


class SubscriberKafka(Runnable):
    def __init__(
        self,
        *,
        kafka_settings: KafkaSettings,
        worker_settings: WorkerSettings,
        callback: Callable,
    ):
        super().__init__()
        self.event_loop = None
        self.consumer = None
        self.kafka_settings = kafka_settings
        self.worker_settings = worker_settings
        self.callback = callback
        self.logger = logging.getLogger("KAFKA_ADAPTER")

    async def run(self):
        self.logger.info("subscribing to kafka")
        # To consume latest messages and auto-commit offsets
        self.consumer = KafkaConsumer(
            self.worker_settings.topic,
            group_id=self.worker_settings.group_id,
            bootstrap_servers=self.kafka_settings.brokers,
        )
        await self.consume()

    async def consume(self):
        for message in self.consumer:
            await self.callback(message)

    def stop(self):
        print("stopping kafka consumer")
        self.consumer.close()
