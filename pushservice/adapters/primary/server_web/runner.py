from pushservice.adapters.primary.runnable_extended import Runnable
from pushservice.settings import WebApiSettings
from fastapi import FastAPI

from .server import RestAPI


class RunnerWeb(Runnable):
    host: str
    port: int

    def __init__(self, settings: WebApiSettings, app: FastAPI):
        super().__init__()
        self.host = settings.host
        self.port = settings.port
        self.server = RestAPI(host=self.host, port=self.port, app=app)

    def run(self):
        # Import your Web Server and run it here
        self.server.run()

    def stop(self) -> None:
        # Stop your Web Server and run it here
        self.server.stop()
