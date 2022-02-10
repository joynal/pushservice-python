import argparse
import asyncio
import json
from dataclasses import asdict
from pushservice.adapters.secondary.persistence_sql.client import (
    create_connection_pool,
)
from pushservice.adapters.secondary.persistence_sql.push_repo import PushRepoSql
from pushservice.adapters.secondary.persistence_sql.site_repo import SiteRepoSql
from pushservice.adapters.secondary.publisher_kafka.client import KafkaPublisher
from pushservice.core.domain.entities import Push
from pushservice.core.domain.entities import Site
from pushservice.core.domain.uuid_encoder import UUIDEncoder
from pushservice.settings import load
from uuid import UUID

parser = argparse.ArgumentParser(description="schedule push script")
parser.add_argument("-n", "--push-id", help="Push id", required=True)
args = parser.parse_args()

settings = load("./settings.yaml")


async def main():
    db_client = await create_connection_pool(settings.database)
    push_repo = PushRepoSql(db_client)
    site_repo = SiteRepoSql(db_client)

    # get push and site then prepare message
    push = await push_repo.get_by_id(entity_id=UUID(args.push_id), data_class=Push)
    site = await site_repo.get_by_id(entity_id=push.site_id, data_class=Site)

    # update database status to processing
    await push_repo.update(entity_id=push.id, update_data={"status": "RUNNING"})

    payload = asdict(push)
    payload["vapid_private_key"] = site.private_key

    # send this data to raw-push
    encode_data = json.dumps(payload, cls=UUIDEncoder).encode("utf-8")
    producer = KafkaPublisher(settings.kafka)
    producer.publish(settings.parser.topic, encode_data)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
