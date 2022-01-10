import logging

from parser.app import Application
from parser.settings import load


def setup_logging(log_level):
    logger = logging.getLogger()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(log_level)


def main():
    settings = load("./settings.yaml")

    setup_logging(log_level=settings.worker.log_level)
    app = Application(settings=settings)

    try:
        app.run()
    except KeyboardInterrupt:
        app.stop()


if __name__ == "__main__":
    main()
