from parser.core.ports.secondary.curd import CrudRepo


class BaseRepoSql(CrudRepo):
    def __init__(self, pool):
        self.pool = pool
        self.query = {}

    async def create(self, entity: tuple):
        async with self.pool.acquire() as conn:
            res = await conn.fetchrow(self.get_query('create'), *entity)
            return res

    async def create_many(self, entity_list: list[tuple]):
        async with self.pool.acquire() as conn:
            res = await conn.executemany(self.get_query('create'), entity_list)
            return res

    def get_query(self, name: str):
        return self.query[name]
