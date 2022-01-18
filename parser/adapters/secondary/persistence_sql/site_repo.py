from .base_repo import BaseRepoSql
from .client import DBClient
from .queries.site import create_site, fetch_site


class SiteRepoSql(BaseRepoSql):
    def __init__(self, db_client: DBClient):
        super().__init__(db_client.pool)
        self.query = {"create": create_site, "fetch": fetch_site}
