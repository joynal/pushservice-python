from abc import ABC, abstractmethod

from pushservice.core.domain.entities import Push


class KafkaMessage(ABC):
    @abstractmethod
    def process(self, push: Push):
        raise NotImplementedError()
