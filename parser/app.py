import logging

from typing import List
from parser.adapters.primary.runnable import Runnable


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

        # Sample:
        #   grpc = RunnerGrpc()
        #   grpc.start()
        #   self.stoppables.append(grpc)

        for x in self.stoppables:
            x.join()

    def stop(self) -> None:
        for x in self.stoppables:
            x.stop()
