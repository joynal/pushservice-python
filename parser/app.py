import logging

from typing import List
from parser.adapters.primary.runnable import Runnable
from parser.adapters.primary.subscriber_kafka.runner import SubscriberKafka
from parser.adapters.secondary.persistence_sql.client import DBClient
from parser.adapters.secondary.persistence_sql.subscriber_repo import SubscriberRepoSql
from parser.core.use_cases.notification import NotificationParser
from parser.settings import Settings, dump_settings


class Application:
    """
    Application object - configure, compose, then run your application
    """

    stoppables: List[Runnable]

    def __init__(self, settings: Settings):
        self.logger = logging.getLogger("Application")
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
            parser = NotificationParser(subscriber_repo)
            parser_stream = SubscriberKafka(self.settings.kafka, parser)
            parser_stream.start()
            self.stoppables.append(parser_stream)

        for x in self.stoppables:
            x.join()

    def stop(self) -> None:
        for x in self.stoppables:
            x.stop()
