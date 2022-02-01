import logging
from typing import Callable

from kafka import KafkaConsumer

from pushservice.adapters.primary.runnable import Runnable
from pushservice.settings import KafkaSettings, TopicSettings


class SubscriberKafka(Runnable):
    def __init__(
            self,
            *,
            kafka_settings: KafkaSettings,
            topic_settings: TopicSettings,
            callback: Callable,
    ):
        super().__init__()
        self.event_loop = None
        self.consumer = None
        self.kafka_settings = kafka_settings
        self.topic_settings = topic_settings
        self.callback = callback
        self.logger = logging.getLogger("KAFKA_ADAPTER")

    async def run(self):
        self.logger.info("subscribing to kafka")
        # To consume latest messages and auto-commit offsets
        self.consumer = KafkaConsumer(
            self.topic_settings.topic,
            group_id=self.topic_settings.group_id,
            bootstrap_servers=self.kafka_settings.brokers,
        )
        await self.consume()

    async def consume(self):
        for message in self.consumer:
            await self.callback(message)

    def stop(self):
        print("stopping kafka consumer")
        self.consumer.close()
