import asyncio

from pushservice.adapters.secondary.persistence_sql.client import (
    create_connection_pool,
)
from pushservice.adapters.secondary.persistence_sql.site_repo import SiteRepoSql
from pushservice.core.domain.vapid import generate_vapid_keypair
from pushservice.settings import load_settings

settings = load_settings("./settings.yaml")


async def main():
    pool = await create_connection_pool(settings.database)
    site_repo = SiteRepoSql(pool)
    keys = generate_vapid_keypair()
    res = await site_repo.create(entity=keys)
    print("site created: ", res)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
