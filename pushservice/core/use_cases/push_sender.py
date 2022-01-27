import json
import logging

from kafka.consumer.fetcher import ConsumerRecord
from pywebpush import webpush, WebPushException

from pushservice.adapters.secondary.persistence_sql.subscriber_repo import SubscriberRepoSql
from pushservice.core.ports.secondary.kafka_message import KafkaMessage


class PushSender(KafkaMessage):
    def __init__(self, subscriber_repo: SubscriberRepoSql):
        self.subscriber_repo = subscriber_repo
        self.logger = logging.getLogger("parser")

    async def process(self, message: ConsumerRecord):
        push_data = json.loads(message.value)
        self.logger.info("received push", push_data)
        del push_data["push_id"]

        try:
            webpush(**push_data)
        except WebPushException as ex:
            print("I'm sorry, Dave, but I can't do that: {}", repr(ex))
            # Mozilla returns additional information in the body of the response.
            if ex.response and ex.response.json():
                extra = ex.response.json()
                print(
                    "Remote service replied with a {}:{}, {}",
                    extra.code,
                    extra.errno,
                    extra.message,
                )
