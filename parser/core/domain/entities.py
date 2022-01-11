from dataclasses import dataclass
from typing import Optional
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
class VapIDKeys:
    p256dh: str
    auth: str


@dataclass
class EndpointUrlData:
    endpoint: str
    expirationTime: Optional[int]
    keys: VapIDKeys


@dataclass
class Subscriber:
    id: UUID
    subscribed: bool
    site_id: UUID
    endpoint: EndpointUrlData


NewPush = tuple[UUID, str, str, dict]


@dataclass
class NotificationOptions:
    body: str
    icon: str


@dataclass
class Notification:
    id: UUID
    site_id: UUID
    title: str
    status: str
    launch_url: str
    priority: str
    time_to_live: int
    options: NotificationOptions


@dataclass
class SendOptions:
    vapidDetails: NewSite
    TTL: int


@dataclass
class NotificationPayload:
    endpoint: EndpointUrlData
    data: Notification
    options: SendOptions
