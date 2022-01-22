import json
import logging
from dataclasses import asdict

from parser.adapters.secondary.kafka_producer.client import KafkaPublisher
from parser.adapters.secondary.persistence_sql.subscriber_repo import SubscriberRepoSql
from parser.core.domain.entities import Subscriber, PushWithKey
from parser.core.domain.uuid_encoder import UUIDEncoder
from parser.core.ports.secondary.push import ProcessPush


from parser.settings import KafkaSettings


def parse_push(push: PushWithKey, producer: KafkaPublisher):
    async def parse(subscriber: Subscriber):
        webpush_payload = {
            "push_id": push.id,
            "subscriber_info": subscriber.subscription_info,
            "ttl": push.time_to_live,
            "vapid_private_key": push.vapid_private_key,
            "vapid_claims": {
                "sub": "https://joynal.dev",
            },
            "data": {
                "title": push.title,
                "launch_url": push.launch_url,
                "priority": push.priority,
                "options": asdict(push.options),
            },
        }

        encode_data = json.dumps(webpush_payload, cls=UUIDEncoder).encode("utf-8")
        # send this data to sender
        # Todo: update sender topic configurable
        producer.publish("send-push", encode_data)

    return parse


class PushParser(ProcessPush):
    def __init__(self, settings: KafkaSettings, subscriber_repo: SubscriberRepoSql):
        self.settings = settings
        self.subscriber_repo = subscriber_repo
        self.logger = logging.getLogger("parser")

    async def process(self, push: PushWithKey):
        self.logger.info("received push", push)
        # TODO: create a callback for subscriber stream
        # TODO: send push object to sender topic
        producer = KafkaPublisher(self.settings)
        await self.subscriber_repo.get_all(
            site_id=push.site_id,
            callback=parse_push(push, producer),
        )
