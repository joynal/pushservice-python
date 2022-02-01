import logging
from typing import List

from pushservice.adapters.primary.runnable import Runnable
from pushservice.adapters.primary.subscriber_kafka.runner import SubscriberKafka
from pushservice.adapters.secondary.persistence_sql.client import DBClient
from pushservice.adapters.secondary.persistence_sql.subscriber_repo import (
    SubscriberRepoSql,
)
from pushservice.core.use_cases.push_parser import PushParser
from pushservice.settings import Settings, dump_settings


class Application:
    """
    Application object - configure, compose, then run your application
    """

    stoppables: List[Runnable]

    def __init__(self, settings: Settings):
        self.logger = logging.getLogger("Parser")
        self.settings = settings
        self.stoppables = []

    async def run(self):
        self.logger.info(
            "Applied configuration:\n" + dump_settings(self.settings),
        )

        db_client = DBClient(self.settings.database)
        await db_client.init()

        if self.settings.kafka.enabled:
            subscriber_repo = SubscriberRepoSql(db_client)
            parser = PushParser(self.settings, subscriber_repo)
            parser_stream = SubscriberKafka(
                kafka_settings=self.settings.kafka,
                topic_settings=self.settings.parser,
                callback=parser.process,
            )
            await parser_stream.run()
            self.stoppables.append(parser_stream)

    def stop(self) -> None:
        for x in self.stoppables:
            x.stop()
