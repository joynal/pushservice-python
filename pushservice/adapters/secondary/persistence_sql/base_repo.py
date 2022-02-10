from dataclasses import dataclass
from pushservice.core.domain.sql import dict_to_sql
from pushservice.core.domain.sql import pyformat_to_sql
from pushservice.core.domain.sql import pyformat_to_sql_many
from pushservice.core.ports.secondary.curd import CrudRepo
from uuid import UUID

from asyncpg import Pool
from dacite import from_dict


class BaseRepoSql(CrudRepo):
    def __init__(self, pool: Pool):
        self.pool = pool
        self.query: dict = {}

    async def create(self, *, entity: dict):
        async with self.pool.acquire() as conn:
            query, values = pyformat_to_sql(self.get_query("create"), entity)
            res = await conn.fetchrow(query, *values)
            return res

    async def get_by_id(self, *, entity_id: UUID, data_class=dataclass):
        async with self.pool.acquire() as conn:
            res = await conn.fetchrow(self.get_query("fetch"), entity_id)
            return from_dict(
                data_class=data_class,
                data={field: value for field, value in res.items()},
            )

    async def create_many(self, *, entity_list: list[dict]):
        async with self.pool.acquire() as conn:
            query, values = pyformat_to_sql_many(self.get_query("create"), entity_list)
            res = await conn.executemany(query, values)
            return res

    async def update(self, *, entity_id: UUID, update_data: dict):
        async with self.pool.acquire() as conn:
            update_placeholder = dict_to_sql(self.get_query("update"), update_data)
            query, values = pyformat_to_sql(
                update_placeholder, {**update_data, "id": entity_id}
            )
            res = await conn.fetchrow(query, *values)
            return res

    async def delete(self, *, entity_id: UUID):
        async with self.pool.acquire() as conn:
            res = await conn.fetchrow(self.get_query("update"), entity_id)
            return res

    def get_query(self, name: str):
        return self.query[name]
