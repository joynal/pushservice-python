# Sample

from python_app_template.adapters.primary.runnable import Runnable

import logging

class RunnerGrpc(Runnable):

    host: str
    port: int

    def __init__(self, settings):
        super().__init__()
        self.logger = logging.getLogger("<YOUR_ADAPTER>")

        self.host = settings.host
        self.port = settings.port

    def run(self):
        # Import your GRPC Server and run it here
        ...

    def stop(self) -> None:
        # Stop your GRPC Server here
        ...