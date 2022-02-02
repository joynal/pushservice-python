import logging
from typing import List

from pushservice.adapters.primary.runnable import Runnable
from pushservice.adapters.primary.subscriber_kafka.runner import SubscriberKafka
from pushservice.adapters.secondary.persistence_sql.client import create_connection_pool
from pushservice.adapters.secondary.persistence_sql.subscriber_repo import (
    SubscriberRepoSql,
)
from pushservice.core.use_cases.push_sender import PushSender
from pushservice.settings import Settings, dump_settings


class Application:
    """
    Application object - configure, compose, then run your application
    """

    stoppables: List[Runnable]

    def __init__(self, settings: Settings):
        self.logger = logging.getLogger("Sender")
        self.settings = settings
        self.stoppables = []

    async def run(self):
        self.logger.info(
            "Applied configuration:\n" + dump_settings(self.settings),
        )

        pool = await create_connection_pool(self.settings.database)

        if self.settings.kafka.enabled:
            subscriber_repo = SubscriberRepoSql(pool)
            sender = PushSender(subscriber_repo)
            parser_stream = SubscriberKafka(
                kafka_settings=self.settings.kafka,
                topic_settings=self.settings.sender,
                callback=sender.process,
            )
            await parser_stream.run()
            self.stoppables.append(parser_stream)

    def stop(self) -> None:
        for x in self.stoppables:
            x.stop()
