import logging

from typing import List
from parser.adapters.primary.runnable import Runnable
from parser.adapters.primary.subscriber_kafka.runner import SubscriberKafka
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

    def run(self):
        self.logger.info(
            "Applied configuration:\n" + dump_settings(self.settings),
        )

        if self.settings.kafka.enabled:
            sub_kafka = SubscriberKafka(self.settings.kafka)
            sub_kafka.start()
            self.stoppables.append(sub_kafka)

        for x in self.stoppables:
            x.join()

    def stop(self) -> None:
        for x in self.stoppables:
            x.stop()
