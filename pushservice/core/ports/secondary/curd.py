from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from uuid import UUID


class CrudRepo(ABC):
    @abstractmethod
    def create(self, *, entity: dict):
        raise NotImplementedError()

    @abstractmethod
    def create_many(self, *, entity_list: list[dict]):
        raise NotImplementedError()

    @abstractmethod
    def get_by_id(self, *, entity_id: UUID, data_class=dataclass):
        raise NotImplementedError()

    @abstractmethod
    def update(self, *, entity_id: UUID, update_data: dict):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, *, entity_id: UUID):
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
