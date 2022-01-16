from kafka import KafkaProducer

from parser.settings import KafkaSettings


class KafkaPublisher:
    def __init__(self, settings: KafkaSettings):
        self.producer = KafkaProducer(bootstrap_servers=settings.brokers)

    def publish(self, topic: str, data: bytes):
        self.producer.send(topic=topic, value=data)
