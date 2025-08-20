import argparse
import asyncio
import math
import random
import secrets

from pushservice.adapters.secondary.persistence_sql.client import (
    create_connection_pool,
)
from pushservice.adapters.secondary.persistence_sql.subscriber_repo import (
    SubscriberRepoSql,
)
from pushservice.settings import load_settings

parser = argparse.ArgumentParser(description="Subscriber generator script")
parser.add_argument("-s", "--site-id", help="Site id for subscribers", required=True)
parser.add_argument(
    "-l", "--length", help="Number of subscribers", default=200000, required=True
)
parser.add_argument("-b", "--batch-size", help="Insertion batch size", default=20000)
args = parser.parse_args()

settings = load_settings("./settings.yaml")


def generate_endpoint():
    push_urls = [
        "https://fcm.googleapis.com/fcm/send/",
        "https://updates.push.services.mozilla.com/wpush/v2/",
    ]
    subscriber_id = (
        secrets.token_urlsafe(10)
        + ":APA91bESNu5qsIA484DSFWyuDLEgMHdAJf45IwMua9lknXrhAzQCrLcN-ZWfT8GE-_"
        + "kxNR6MiCq1tfPr1aKWH8bVFNm6bmtDY-xHug-B76h6IqwemtB9tnlPsTqlr9A8ZcvA3dZzlxMc"
    )
    return {
        "endpoint": random.choice(push_urls) + subscriber_id,
        "expirationTime": None,
        "keys": {
            "p256dh": "BHk1DzprVgT26pIBTc3gsm-xE1m-DZzZcn_"
            + "xAnvEpGKBMkja3V5rQsFQuQ7wlJV6I0A2P5LVHtjhp7lYZPsoQ8E",
            "auth": "mrLLfPc_dIlwsO521ix1bQ",
        },
    }


async def main():
    pool = await create_connection_pool(settings.database)
    subscriber_repo = SubscriberRepoSql(pool)
    length = int(args.length)
    batch_size = int(args.batch_size)
    range_num = math.ceil(length / batch_size) or 1
    for batch_num in range(range_num):
        subscribers = []
        batch_size = length if (length < batch_size) else batch_size
        for _ in range(int(batch_size)):
            subscribers.append(
                {"site_id": args.site_id, "subscription_info": generate_endpoint()}
            )
        length -= batch_size
        await subscriber_repo.create_many(entity_list=subscribers)
        print("batch inserted: ", batch_num + 1)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
