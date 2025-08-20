import asyncio
import logging

from pushservice.settings import load_settings
from sender.app import Application


def setup_logging(log_level):
    logger = logging.getLogger()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(log_level)


async def main():
    settings = load_settings("./settings.yaml")

    setup_logging(log_level=settings.sender.log_level)
    app = Application(settings=settings)

    try:
        await app.run()
    except KeyboardInterrupt:
        app.stop()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
