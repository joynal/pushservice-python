import asyncio

from parser.adapters.secondary.persistence_sql.client import DBClient
from parser.adapters.secondary.persistence_sql.site_repo import SiteRepoSql
from parser.core.domain.vapid import generate_vapid_keypair
from parser.settings import load

settings = load("./settings.yaml")


async def main():
    db_client = DBClient(settings.database)
    await db_client.init()
    site_repo = SiteRepoSql(db_client)
    keys = generate_vapid_keypair()
    res = await site_repo.create(entity=keys)
    print("site created: ", res)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
