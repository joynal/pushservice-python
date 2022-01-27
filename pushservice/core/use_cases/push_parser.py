import json
import logging
from dataclasses import asdict
from uuid import UUID

import dacite
from dacite import from_dict
from kafka.consumer.fetcher import ConsumerRecord

from pushservice.settings import Settings
from pushservice.adapters.secondary.publisher_kafka.client import KafkaPublisher
from pushservice.adapters.secondary.persistence_sql.subscriber_repo import SubscriberRepoSql
from pushservice.core.domain.entities import Subscriber, PushWithKey
from pushservice.core.domain.uuid_encoder import UUIDEncoder
from pushservice.core.ports.secondary.kafka_message import KafkaMessage


class PushParser(KafkaMessage):
    def __init__(self, settings: Settings, subscriber_repo: SubscriberRepoSql):
        self.kafka_settings = settings.kafka
        self.sender_settings = settings.sender
        self.subscriber_repo = subscriber_repo
        self.producer = KafkaPublisher(self.kafka_settings)
        self.logger = logging.getLogger("parser")

    def parse_push(self, push: PushWithKey):
        async def parse(subscriber: Subscriber):
            webpush_payload = {
                "push_id": push.id,
                "subscription_info": subscriber.subscription_info,
                "ttl": push.time_to_live,
                "vapid_private_key": push.vapid_private_key,
                "vapid_claims": {
                    "sub": "https://joynal.dev",
                },
                "data": json.dumps({
                    "title": push.title,
                    "launch_url": push.launch_url,
                    "priority": push.priority,
                    "options": asdict(push.options),
                }),
            }

            encode_data = json.dumps(webpush_payload, cls=UUIDEncoder).encode("utf-8")
            # send this data to sender
            self.producer.publish(self.sender_settings.topic, encode_data)

        return parse

    async def process(self, message: ConsumerRecord):
        push = from_dict(
            data_class=PushWithKey,
            data=json.loads(message.value),
            config=dacite.Config(cast=[UUID]),
        )
        self.logger.info("received push", push)
        await self.subscriber_repo.get_all(
            site_id=push.site_id,
            callback=self.parse_push(push),
        )
