from abc import ABC
from abc import abstractmethod
from threading import Thread


class Runnable(ABC, Thread):
    @abstractmethod
    def run(self) -> None:
        """
        This method is intented as the entry point for
        starting and running a primary adapter.
        """
        raise NotImplementedError()

    @abstractmethod
    def stop(self) -> None:
        """
        Stop adapter from running anymore
        """
        raise NotImplementedError("Primary adapter does not implement Stop method")
