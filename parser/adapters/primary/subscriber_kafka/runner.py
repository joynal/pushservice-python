import asyncio
import json
import logging

from dacite import from_dict
from kafka import KafkaConsumer

from parser.adapters.primary.runnable import Runnable
from parser.core.domain.entities import Notification
from parser.core.use_cases.notification import NotificationParser
from parser.settings import KafkaSettings


class SubscriberKafka(Runnable):
    def __init__(self, settings: KafkaSettings, parser: NotificationParser):
        super().__init__()
        self.event_loop = None
        self.consumer = None
        self.settings = settings
        self.parser = parser
        self.logger = logging.getLogger("KAFKA_ADAPTER")

    def run(self):
        self.logger.info("subscribing to kafka")
        # To consume latest messages and auto-commit offsets
        self.consumer = KafkaConsumer(
            self.settings.topic,
            group_id=self.settings.group_id,
            bootstrap_servers=self.settings.brokers,
        )
        self.consumer_loop()

    def consumer_loop(self):
        try:
            self.event_loop = asyncio.get_running_loop()
        except RuntimeError:
            self.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.event_loop)
        self.event_loop.run_until_complete(self.consume())

    async def consume(self):
        for message in self.consumer:
            notification = from_dict(
                data_class=Notification, data=json.loads(message.value)
            )
            await self.parser.process(notification)

    def stop(self):
        print("stopping kafka consumer")
        self.consumer.close()
