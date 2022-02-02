import json
import logging

from kafka.consumer.fetcher import ConsumerRecord
from pywebpush import webpush, WebPushException

from pushservice.adapters.secondary.persistence_sql.subscriber_repo import (
    SubscriberRepoSql,
)
from pushservice.core.ports.secondary.kafka_message import KafkaMessage


class PushSender(KafkaMessage):
    def __init__(self, subscriber_repo: SubscriberRepoSql):
        self.subscriber_repo = subscriber_repo
        self.logger = logging.getLogger("parser")

    async def process(self, message: ConsumerRecord):
        push_data = json.loads(message.value)
        del push_data["push_id"]

        try:
            webpush(**push_data)
        except WebPushException as ex:
            self.logger.error(repr(ex))
