from abc import ABC
from abc import abstractmethod
from pushservice.core.domain.entities import Push


class KafkaMessage(ABC):
    @abstractmethod
    def process(self, push: Push):
        raise NotImplementedError()
