import logging

from kafka import KafkaConsumer

from parser.adapters.primary.runnable import Runnable
from parser.settings import KafkaSettings


class SubscriberKafka(Runnable):
    def __init__(self, settings: KafkaSettings):
        super().__init__()
        self.consumer = None
        self.settings = settings
        self.logger = logging.getLogger("KAFKA_ADAPTER")

    def run(self):
        self.logger.info("subscribing to kafka")
        # To consume latest messages and auto-commit offsets
        self.consumer = KafkaConsumer(
            self.settings.topic,
            group_id=self.settings.group_id,
            bootstrap_servers=self.settings.brokers
        )

        for message in self.consumer:
            self.logger.info("message:", message)
            self.logger.info("message_value:", message.value)

    def stop(self):
        print("stopping kafka consumer")
        self.consumer.close()
