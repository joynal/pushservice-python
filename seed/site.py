import asyncio

from parser.adapters.secondary.persistence_sql.client import DBClient
from parser.adapters.secondary.persistence_sql.site_repo import SiteRepoSql
from parser.core.domain.entities import NewSite
from parser.core.domain.vapid import generate_vapid_keypair
from parser.settings import load_settings

settings = load_settings("./settings.yaml")


async def main():
    db_client = DBClient(settings.database)
    await db_client.init()
    site_repo = SiteRepoSql(db_client)
    keys = generate_vapid_keypair()
    res = await site_repo.create((keys['public_key'], keys['private_key']))
    print("site created: ", res)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
