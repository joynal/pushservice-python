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


@dataclass
class NewSubscriber:
    site_id: UUID
    subscription_info: dict


@dataclass
class Subscriber(NewSubscriber):
    id: UUID
    subscribed: bool


NewPush = tuple[UUID, str, str, dict]


@dataclass
class PushOptions:
    body: str
    icon: str


@dataclass
class Push:
    id: UUID
    site_id: UUID
    title: str
    status: str
    launch_url: str
    priority: str
    time_to_live: int
    options: PushOptions


@dataclass
class PushWithKey(Push):
    vapid_private_key: str


@dataclass
class WebpushData:
    title: str
    launch_url: str
    priority: str
    options: PushOptions


@dataclass
class WebpushPayload:
    push_id: UUID
    subscription_info: dict
    data: WebpushData
    ttl: int
    vapid_private_key: str
    vapid_claims: dict
