import asyncio
from uuid import UUID

from pushservice.adapters.secondary.persistence_sql.client import (
    create_connection_pool,
)
from pushservice.adapters.secondary.persistence_sql.subscriber_repo import (
    SubscriberRepoSql,
)
from pushservice.settings import load_settings

settings = load_settings("./settings.yaml")


async def process_subscriber(subscriber):
    print(subscriber)


async def main():
    pool = await create_connection_pool(settings.database)
    subscriber_repo = SubscriberRepoSql(pool)
    await subscriber_repo.get_all(
        site_id=UUID("83662cf4-424b-4bb8-99f0-78b2eeeaa0b8"),
        callback=process_subscriber,
    )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
