from abc import ABC, abstractmethod

from parser.core.domain.entities import Notification


class ProcessNotification(ABC):
    @abstractmethod
    def process(self, notification: Notification):
        raise NotImplementedError()
