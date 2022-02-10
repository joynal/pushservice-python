from asyncpg import Pool

from .base_repo import BaseRepoSql
from .queries.site import create_site
from .queries.site import fetch_site


class SiteRepoSql(BaseRepoSql):
    def __init__(self, pool: Pool):
        super().__init__(pool)
        self.query = {"create": create_site, "fetch": fetch_site}
