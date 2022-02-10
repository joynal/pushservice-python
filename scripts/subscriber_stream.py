import asyncio
from pushservice.adapters.secondary.persistence_sql.client import (
    create_connection_pool,
)
from pushservice.adapters.secondary.persistence_sql.subscriber_repo import (
    SubscriberRepoSql,
)
from pushservice.settings import load
from uuid import UUID

settings = load("./settings.yaml")


async def process_subscriber(subscriber):
    print(subscriber)


async def main():
    pool = await create_connection_pool(settings.database)
    subscriber_repo = SubscriberRepoSql(pool)
    await subscriber_repo.get_all(
        site_id=UUID("3f7230bd-af13-4b9b-a351-e00e7429bf78"),
        callback=process_subscriber,
    )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
