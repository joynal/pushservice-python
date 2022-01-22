from abc import ABC, abstractmethod

from parser.core.domain.entities import Push


class ProcessPush(ABC):
    @abstractmethod
    def process(self, push: Push):
        raise NotImplementedError()
