from abc import ABC, abstractmethod
from uuid import UUID


class CrudRepo(ABC):
    @abstractmethod
    def create(self, entity):
        raise NotImplementedError()

    @abstractmethod
    def create_many(self, entity_list: list[tuple]):
        raise NotImplementedError()

    @abstractmethod
    def get_by_id(self, entity_id: UUID):
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity_id: UUID, entity: dict):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, entity_id):
        raise NotImplementedError()

    # @abstractmethod
    # def get_many_by_id(self, entity_ids):
    #     raise NotImplementedError()
    #
    # @abstractmethod
    # def get_all(self):
    #     raise NotImplementedError()
    #

    # @abstractmethod
    # def diff(self, entity):
    #     raise NotImplementedError()
    #
    # @abstractmethod
    # def upsert(self, entity):
    #     raise NotImplementedError()
