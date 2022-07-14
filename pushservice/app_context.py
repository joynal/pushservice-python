from contextvars import ContextVar
from types import SimpleNamespace
from uuid import UUID
from timeit import default_timer


Defaults = SimpleNamespace(
    number=-1,
    id=UUID("00000000-0000-0000-0000-000000000000"),
    text="unknown",
)

Keys = SimpleNamespace(
    trace_id="trace_id",
    request_id="request_id",
    path="path",
    method="method",
    request_begin="request_begin",
    customer_id="customer_id",
    reseller_id="reseller_id",
)

_trace_id: ContextVar[UUID] = ContextVar(Keys.trace_id, default=Defaults.id)
_request_id: ContextVar[UUID] = ContextVar(Keys.request_id, default=Defaults.id)
_path: ContextVar[str] = ContextVar(Keys.path, default=Defaults.text)
_method: ContextVar[str] = ContextVar(Keys.method, default=Defaults.text)
_request_begin: ContextVar[float] = ContextVar(Keys.request_begin, default=Defaults.number)


def set_request_begin() -> None:
    begin = default_timer()
    _request_begin.set(begin)


def set_trace_id(value: UUID) -> None:
    _trace_id.set(value)


def get_trace_id() -> UUID:
    return _trace_id.get()


def set_request_id(value: UUID) -> None:
    _request_id.set(value)


def get_request_id() -> UUID:
    return _request_id.get()


def set_path(value: str) -> None:
    _path.set(value)


def get_path() -> str:
    return _path.get()


def set_method(value: str) -> None:
    _method.set(value)


def get_method() -> str:
    return _method.get()


def get_request_begin() -> float:
    return _request_begin.get()

