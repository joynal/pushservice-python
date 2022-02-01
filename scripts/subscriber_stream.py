import asyncio
from uuid import UUID

from pushservice.adapters.secondary.persistence_sql import DBClient
from pushservice.adapters.secondary.persistence_sql import SubscriberRepoSql
from pushservice.settings import load

settings = load("./settings.yaml")


async def process_subscriber(subscriber):
    print(subscriber)


async def main():
    db_client = DBClient(settings.database)
    await db_client.init()
    subscriber_repo = SubscriberRepoSql(db_client)
    await subscriber_repo.get_all(
        site_id=UUID("3f7230bd-af13-4b9b-a351-e00e7429bf78"),
        callback=process_subscriber,
    )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
