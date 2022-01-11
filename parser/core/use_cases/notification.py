from parser.core.domain.entities import Notification
from parser.core.ports.secondary.notification import ProcessNotification


class PrepareNotification(ProcessNotification):
    def __init__(self, kafka, subscriber_repo):
        self.kafka = kafka
        self.subscriber_repo = subscriber_repo

    def process(self, notification: Notification):
        print("process data")
