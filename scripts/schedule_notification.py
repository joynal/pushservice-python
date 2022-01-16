import argparse
import asyncio
import json
from dataclasses import asdict
from uuid import UUID

from dacite import from_dict

from parser.adapters.secondary.kafka_producer.client import KafkaPublisher
from parser.adapters.secondary.persistence_sql.client import DBClient
from parser.adapters.secondary.persistence_sql.push_repo import PushRepoSql
from parser.adapters.secondary.persistence_sql.site_repo import SiteRepoSql
from parser.core.domain.entities import Site, Notification
from parser.settings import load

parser = argparse.ArgumentParser(description="schedule notification script")
parser.add_argument("-n", "--notification-id", help="Notification id", required=True)
args = parser.parse_args()

settings = load("./settings.yaml")


async def main():
    db_client = DBClient(settings.database)
    await db_client.init()
    push_repo = PushRepoSql(db_client)
    site_repo = SiteRepoSql(db_client)

    # get notification and site then prepare message
    res_notification = await push_repo.get_by_id(entity_id=UUID(args.notification_id))
    notification = from_dict(
        data_class=Notification, data={field: value for field, value in res_notification.items()}
    )
    res_site = await site_repo.get_by_id(entity_id=notification["site_id"])
    site = from_dict(
        data_class=Site, data={field: value for field, value in res_site.items()}
    )
    notification.vapid_private_key = site.private_key

    # update database status to processing
    await push_repo.update(entity_id=notification.id, update_data={"status": "RUNNING"})

    # send this data to raw-notification
    encode_data = json.dumps(asdict(notification)).encode('utf-8')
    producer = KafkaPublisher(settings.kafka)
    producer.publish(settings.kafka.topic, encode_data)

    if __name__ == "__main__":
        loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
