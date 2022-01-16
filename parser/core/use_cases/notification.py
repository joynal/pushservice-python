import logging

from parser.adapters.secondary.persistence_sql.subscriber_repo import SubscriberRepoSql
from parser.core.domain.entities import Notification, Subscriber
from parser.core.ports.secondary.notification import ProcessNotification


def parse_notification(notification: Notification):
    async def parse(subscriber: Subscriber):
        print("subscriber: ", subscriber)
        print("notification: ", notification)

    return parse


class NotificationParser(ProcessNotification):
    def __init__(self, subscriber_repo: SubscriberRepoSql):
        self.subscriber_repo = subscriber_repo
        self.logger = logging.getLogger("parser")

    async def process(self, notification: Notification):
        self.logger.info("received notification")
        self.logger.info(notification)
        # TODO: create a callback for subscriber stream
        # TODO: send notification object to sender topic
        await self.subscriber_repo.get_all(
            site_id=notification.site_id,
            callback=parse_notification(notification)
        )
