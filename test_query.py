import asyncio

from parser.adapters.secondary.persistence_sql.client import DBClient
from parser.adapters.secondary.persistence_sql.subscriber_repo import SubscriberRepoSql
from parser.settings import load

settings = load("./settings.yaml")


async def main():
    db_client = DBClient(settings.database)
    await db_client.init()
    subscriber_repo = SubscriberRepoSql(db_client)
    await subscriber_repo.subscriber_stream()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
