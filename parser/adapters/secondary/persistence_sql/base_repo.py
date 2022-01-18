from uuid import UUID

from parser.core.domain.sql import dict_to_sql, pyformat_to_sql, pyformat_to_sql_many
from parser.core.ports.secondary.curd import CrudRepo


class BaseRepoSql(CrudRepo):
    def __init__(self, pool):
        self.pool = pool
        self.query = {}

    async def create(self, *, entity: dict):
        async with self.pool.acquire() as conn:
            query, values = pyformat_to_sql(self.get_query("create"), entity)
            res = await conn.fetchrow(query, *values)
            return res

    async def get_by_id(self, *, entity_id: UUID):
        async with self.pool.acquire() as conn:
            res = await conn.fetchrow(self.get_query("fetch"), entity_id)
            return res

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
