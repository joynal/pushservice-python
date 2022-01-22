import json
import logging
from uuid import UUID

import dacite
from dacite import from_dict
from kafka import KafkaConsumer

from parser.adapters.primary.runnable import Runnable
from parser.core.domain.entities import PushWithKey
from parser.core.use_cases.push import PushParser
from parser.settings import KafkaSettings


class SubscriberKafka(Runnable):
    def __init__(self, settings: KafkaSettings, parser: PushParser):
        super().__init__()
        self.event_loop = None
        self.consumer = None
        self.settings = settings
        self.parser = parser
        self.logger = logging.getLogger("KAFKA_ADAPTER")

    async def run(self):
        self.logger.info("subscribing to kafka")
        # To consume latest messages and auto-commit offsets
        self.consumer = KafkaConsumer(
            self.settings.topic,
            group_id=self.settings.group_id,
            bootstrap_servers=self.settings.brokers,
        )
        await self.consume()

    async def consume(self):
        for message in self.consumer:
            push = from_dict(
                data_class=PushWithKey,
                data=json.loads(message.value),
                config=dacite.Config(cast=[UUID]),
            )
            await self.parser.process(push)

    def stop(self):
        print("stopping kafka consumer")
        self.consumer.close()
