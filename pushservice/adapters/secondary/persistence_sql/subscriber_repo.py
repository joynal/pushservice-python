from uuid import UUID

from dacite import from_dict

from pushservice.core.domain.entities import Subscriber
from .base_repo import BaseRepoSql
from .client import DBClient
from .queries.subscriber import create_subscriber, fetch_stream, fetch_subscriber


class SubscriberRepoSql(BaseRepoSql):
    def __init__(self, db_client: DBClient):
        super().__init__(db_client.pool)
        self.query = {
            "create": create_subscriber,
            "fetch": fetch_subscriber,
            "fetch_stream": fetch_stream,
        }

    async def get_all(self, *, site_id: UUID, callback):
        async with self.pool.acquire() as conn:
            stmt = await conn.prepare(self.get_query("fetch_stream"))
            async with conn.transaction():
                async for record in stmt.cursor(site_id):
                    subscriber = from_dict(data_class=Subscriber, data=record)
                    await callback(subscriber)
