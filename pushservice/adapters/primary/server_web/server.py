from pushservice import monitor
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from uvicorn import Config
from uvicorn import Server

from .exceptions import ApiException
from .routes import health, push


class UvicornServer(Server):
    def install_signal_handlers(self):
        """
        UvicornServer implements a signal handler for handling interrupts
        We are making our own thread and handling the signals at top
        level of the application. Therefore we do not want this behaviour
        """
        pass  # Override of function with no behaviour

    def run_forever(self):
        self.run()


class RestAPI:
    def __init__(self, host: str, port: int, app: FastAPI):
        self.host = host
        self.port = port
        self.uvicorn_instance = UvicornServer(
            Config(app, host=host, port=port, reload=True, debug=False)
        )

        @app.exception_handler(ApiException)
        async def http_exception_handler(request, exc):
            return JSONResponse(
                status_code=exc.status_code,
                content={"errors": [{"status": exc.status_code, "detail": exc.detail}]},
            )

        app.include_router(health.router, prefix="/api/v1")
        app.include_router(push.router, prefix="/api/v1")

    def stop(self) -> None:
        # self.logger.info("Stopping FASTAPI")
        self.uvicorn_instance.should_exit = True
        monitor.WebServer.app_ended()

    def run(self):
        monitor.WebServer.app_started(self.host, self.port)
        self.uvicorn_instance.run_forever()
        monitor.WebServer.app_ended()
