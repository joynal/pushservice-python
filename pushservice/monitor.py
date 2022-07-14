from __future__ import annotations

import json
import logging
import uuid
from timeit import default_timer

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install

from pushservice import app_context
from pushservice.settings import MonitorSettings

logger: logging.Logger | None = None


def init(settings: MonitorSettings):
    """
    Init all monitoring mechanisms.
    Only intended to be called once on application setup.
    """
    global logger

    if logger is not None:
        _warning("Logger already initialized")
        return

    install()
    rich_handler = RichHandler(
        console=Console(color_system="standard", width=180),
        rich_tracebacks=True,
    )
    logging.basicConfig(
        level=settings.log_level,
        format="%(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S.%f]",
        handlers=[rich_handler],
    )
    logger = logging.getLogger()
    _info("Logger initialized")


def _info(msg: str):
    _log(level=logging.INFO, msg=msg)


def _warning(msg: str):
    _log(level=logging.WARNING, msg=msg)


def _error(msg: str):
    _log(level=logging.ERROR, msg=msg, exc_info=True)


def _debug(msg: str):
    _log(level=logging.DEBUG, msg=msg)


def _log(level: int, msg: str, **kwargs):
    if logger is not None:
        labels = {"path": app_context.get_path()}

        if app_context.get_method() != app_context.Defaults.text:
            labels["method"] = app_context.get_method()

        kwargs["extra"] = {
            "trace": app_context.get_trace_id(),
            "span_id": app_context.get_request_id(),
            "insert_id": uuid.uuid4(),
            "labels": labels,
        }
        logger.log(level, msg, **kwargs)


class App:
    @staticmethod
    def composition_started():
        _info("Composing the application...")

    @staticmethod
    def start():
        _info("Back Office application starting...")

    @staticmethod
    def end():
        _info("Back Office application ended")

    @staticmethod
    def publish_settings(settings: [str]):
        _info("CURRENT SERVER SETTINGS | START")
        [_info(setting) for setting in settings()]
        _info("CURRENT SERVER SETTINGS | END")

    @staticmethod
    def critical_fault(e: Exception):
        _error(f"Critical fault encountered - abandon ye of all hope... {e}")


class PersistenceSQL:
    @staticmethod
    def failed_to_get_psycopg_connection_from_pool(e):
        _error(
            f"Failed to retrieve a psycopg connection from the connection pool... {e}"
        )

    @staticmethod
    def created_aiopg_pool(masked_conn_string: str):
        _info(
            f"Created an aiopg connection pool for the"
            f" connection string: {masked_conn_string}"
        )

    @staticmethod
    def could_not_create_psycopg_connection(e):
        _warning(f"Failed to create a psycopg connection... {e}")


class GrpcServer:
    @staticmethod
    def address_has_non_numeric_number(address_id, e):
        _warning(
            f"Address with id {address_id} has non numeric number field. Error: {e}"
        )

    @staticmethod
    def latency_wrapper_error(e):
        _error(f"Error encountered in the grpc server latency wrapper: {e}")

    @staticmethod
    def request_started():
        _info(f"gRPC {app_context.get_path()} request started")

    @staticmethod
    def log_current_customer(customer_name):
        name = customer_name if customer_name else "unknown"
        _info(f"Customer name '{name}'")

    @staticmethod
    def request_ended():
        start = app_context.get_request_begin()

        if start == app_context.Defaults.number:
            _warning(
                f"Cannot time request, check "
                f"{app_context.set_request_begin.__name__} is called!"
            )
            _info(f"gRPC {app_context.get_path()} request finished")
        else:
            end = default_timer()
            duration = round((end - start) * 1000, 2)
            _info(f"gRPC {app_context.get_path()} request finished after {duration}ms")

    @staticmethod
    def app_started(host, port):
        _info(f"GRPC interface on {host}:{port} starting...")

    @staticmethod
    def app_ended(host, port):
        _info(f"GRPC interface on {host}:{port} stopped!")

    @staticmethod
    def shutdown_requested():
        _info("GRPC interface shutdown requested...")

    @staticmethod
    def dump_request_params(request):
        # note the actual limit in GCP appears to be 102,400 characters
        limit = 8192

        text = str(request)
        is_too_big = len(text) > limit

        size = len(text.encode("utf-8"))
        _info(f"GRPC request is {size} bytes")

        if is_too_big:
            _info(f"GRPC request (truncated): {text[:limit]}")
        else:
            _info(f"GRPC request: {text}")


class WebServer:
    @staticmethod
    def app_started(host, port):
        _info(f"Web server on {host}:{port} starting...")

    @staticmethod
    def app_ended():
        _info("Web server stopped!")

    @staticmethod
    def shutdown_requested():
        _info("Web server shutdown requested...")

    @staticmethod
    def access_token_issuer_missing():
        _warning("The issuer 'iss' is not present on the access token")

    @staticmethod
    def xtoken_not_present():
        _warning("X-Token header is not present on incoming request")

    @staticmethod
    def validation_errors(info, errors):
        _warning(f"Error(s) occurred during '{info}': {errors}")

    @staticmethod
    def request_started():
        _info(
            f"Web request [{app_context.get_method()}] "
            f"started on path: '{app_context.get_path()}'"
        )

    @staticmethod
    def log_current_reseller(reseller_name):
        name = reseller_name if reseller_name else "unknown"
        _info(f"Reseller name '{name}'")

    @staticmethod
    def request_ended():
        start = app_context.get_request_begin()

        if start == app_context.Defaults.number:
            _warning(
                f"Cannot time request, check "
                f"{app_context.set_request_begin.__name__} is called!"
            )
            _info(f"Web request '{app_context.get_path()}' finished")
        else:
            end = default_timer()
            duration = round((end - start) * 1000, 2)
            _info(f"Web request '{app_context.get_path()}' finished after {duration}ms")

    @staticmethod
    def dump_query_string(query_string):
        if query_string:
            _info(f"Request query string: {bytes.decode(query_string)}")

    @staticmethod
    def dump_body(body):
        _info("Request body on next line...")
        _info(json.dumps(body))
