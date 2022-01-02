from .base_repo import BaseRepoSql
from .client import DBClient
from .queries.subscriber import create_subscriber


class SubscriberRepoSql(BaseRepoSql):
    def __init__(self, db_client: DBClient):
        super().__init__(db_client.pool)
        self.query = {
            "create": create_subscriber
        }
