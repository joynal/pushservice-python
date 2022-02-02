import argparse
import asyncio

from pushservice.adapters.secondary.persistence_sql.client import create_connection_pool
from pushservice.adapters.secondary.persistence_sql.push_repo import PushRepoSql
from pushservice.settings import load

parser = argparse.ArgumentParser(description="Push generator script")
parser.add_argument("-s", "--site-id", help="Site id for push", required=True)
args = parser.parse_args()

settings = load("./settings.yaml")


async def main():
    pool = await create_connection_pool(settings.database)
    push_repo = PushRepoSql(pool)

    push = {
        "site_id": args.site_id,
        "title": "I came from demo",
        "launch_url": "https://joynal.dev",
        "options": {
            "body": "Ignore it, it's a test push",
            "icon": "https://avatars3.githubusercontent.com/u/6458212",
        },
    }

    res = await push_repo.create(entity=push)
    print("push created", res)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
