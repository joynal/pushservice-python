from asyncpg import Pool

from .base_repo import BaseRepoSql
from .queries.push import create_push
from .queries.push import delete_push
from .queries.push import fetch_push
from .queries.push import update_push


class PushRepoSql(BaseRepoSql):
    def __init__(self, pool: Pool):
        super().__init__(pool)
        self.query = {
            "create": create_push,
            "fetch": fetch_push,
            "update": update_push,
            "delete": delete_push,
        }
