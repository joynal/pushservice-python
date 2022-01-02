from dataclasses import dataclass
from uuid import UUID


@dataclass
class NewSite:
    public_key: str
    private_key: str


class Site(NewSite):
    id: UUID
    public_key: str
    private_key: str


NewSubscriber = tuple[UUID, dict]


@dataclass
class Subscriber:
    id: UUID
    subscribed: bool
    site_id: UUID
    endpoint: dict


NewPush = tuple[UUID, str, str, dict]


@dataclass
class Push:
    id: UUID
    title: str
    launch_url: str
    options: dict
