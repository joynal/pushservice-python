from .base_repo import BaseRepoSql
from .client import DBClient
from .queries.push import create_push, fetch_push, update_push, delete_push


class PushRepoSql(BaseRepoSql):
    def __init__(self, db_client: DBClient):
        super().__init__(db_client.pool)
        self.query = {
            'create': create_push,
            'fetch': fetch_push,
            'update': update_push,
            'delete': delete_push,
        }
