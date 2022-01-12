from .base_repo import BaseRepoSql
from .client import DBClient
from .queries.subscriber import create_subscriber, fetch_stream


class SubscriberRepoSql(BaseRepoSql):
    def __init__(self, db_client: DBClient):
        super().__init__(db_client.pool)
        self.query = {
            "create": create_subscriber,
            "fetch_stream": fetch_stream
        }

    async def subscriber_stream(self):
        async with self.pool.acquire() as conn:
            stmt = await conn.prepare(self.get_query('fetch_stream'))
            async with conn.transaction():
                async for record in stmt.cursor('c540eac3-a97b-4a22-a0b1-88475e9fe4e9'):
                    print(record)
