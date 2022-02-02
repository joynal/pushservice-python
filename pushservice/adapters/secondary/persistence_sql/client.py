import logging

import asyncpg
from asyncpg import Pool

from pushservice.core.domain.jsonb import jsonb_encoder, jsonb_decoder

logger = logging.getLogger("DB_CLIENT")


async def set_codec(conn):
    await conn.set_type_codec(
        "jsonb",
        schema="pg_catalog",
        format="binary",
        encoder=jsonb_encoder,
        decoder=jsonb_decoder,
    )


async def create_connection_pool(settings) -> Pool:
    try:
        pool = await asyncpg.create_pool(
            dsn=settings.connection_string,
            min_size=settings.pool_min_size,
            max_size=settings.pool_max_size,
            max_queries=settings.max_queries,
            init=set_codec,
        )
        return pool
    except Exception as exp:
        logger.error("Initialize error: ", repr(exp))
