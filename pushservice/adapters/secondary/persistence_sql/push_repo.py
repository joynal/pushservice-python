from asyncpg import Pool

from .base_repo import BaseRepoSql
from .queries.push import create_push, fetch_push, update_push, delete_push


class PushRepoSql(BaseRepoSql):
    def __init__(self, pool: Pool):
        super().__init__(pool)
        self.query = {
            "create": create_push,
            "fetch": fetch_push,
            "update": update_push,
            "delete": delete_push,
        }
