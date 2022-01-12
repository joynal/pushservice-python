from dataclasses import dataclass

import asyncpg

from parser.core.domain.jsonb import jsonb_encoder, jsonb_decoder
from parser.settings import DatabaseSettings


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
                dsn=self.settings.connection_string,
                min_size=self.settings.pool_min_size,
                max_size=self.settings.pool_max_size,
                max_queries=self.settings.max_queries,
                init=set_codec
            )
        except Exception as exp:
            print("Initialize error: ", exp)
