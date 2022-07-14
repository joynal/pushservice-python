import logging
from typing import List

from pushservice.adapters.primary.runnable_extended import Runnable
from pushservice.adapters.primary.server_web.factory import create_app
from pushservice.adapters.primary.server_web.runner import RunnerWeb


class Application:
    """
    Application object - configure, compose, then run your application
    """

    stoppables: List[Runnable]

    def __init__(self, settings):
        self.logger = logging.getLogger("Application")
        self.settings = settings
        self.stoppables = []

    def run(self):
        # For each primary adapter you have, initialize it, start it,
        # then add it to stoppable

        if self.settings.web_api.enabled:
            web = RunnerWeb(settings=self.settings.web_api, app=create_app())
            web.start()
            self.stoppables.append(web)

        for x in self.stoppables:
            x.join()

    def stop(self) -> None:
        for x in self.stoppables:
            x.stop()
