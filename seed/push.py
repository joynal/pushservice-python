import argparse
import asyncio

from parser.adapters.secondary.persistence_sql.client import DBClient
from parser.adapters.secondary.persistence_sql.push_repo import PushRepoSql
from parser.settings import load

parser = argparse.ArgumentParser(description="Push generator script")
parser.add_argument("-s", "--site-id", help="Site id for push", required=True)
args = parser.parse_args()

settings = load("./settings.yaml")


async def main():
    db_client = DBClient(settings.database)
    await db_client.init()
    push_repo = PushRepoSql(db_client)
    options = {
        "body": "Ignore it, it's a test notification",
        "icon": "https://avatars3.githubusercontent.com/u/6458212",
    }
    res = await push_repo.create((args.site_id, "I came from demo", "https://joynal.dev", options))
    print("push created", res)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
