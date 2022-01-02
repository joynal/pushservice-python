from dataclasses import dataclass

import asyncpg

from parser.core.domain.jsonb import jsonb_encoder, jsonb_decoder


@dataclass
class DatabaseSettings:
    connection_uri: str
    pool_min_size: int = 5
    pool_max_size: int = 10
    max_queries: int = 100000


async def set_codec(conn):
    await conn.set_type_codec(
        'jsonb',
        schema='pg_catalog',
        format='binary',
        encoder=jsonb_encoder,
        decoder=jsonb_decoder,
    )


class DBClient:
    def __init__(self, settings: DatabaseSettings):
        self.pool = None
        self.settings = settings

    async def init(self):
        try:
            self.pool = await asyncpg.create_pool(
                dsn=self.settings.connection_uri,
                min_size=self.settings.pool_min_size,
                max_size=self.settings.pool_max_size,
                max_queries=self.settings.max_queries,
                init=set_codec
            )
        except Exception as exp:
            print("Initialize error: ", exp)
