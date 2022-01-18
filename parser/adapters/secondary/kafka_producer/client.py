from kafka import KafkaProducer

from parser.settings import KafkaSettings


def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


class KafkaPublisher:
    def __init__(self, settings: KafkaSettings):
        self.producer = KafkaProducer(bootstrap_servers=settings.brokers)

    def publish(self, topic: str, data: bytes):
        self.producer.send(topic=topic, value=data).add_callback(on_send_success)
