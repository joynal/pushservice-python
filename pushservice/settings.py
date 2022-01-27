import logging
from dataclasses import dataclass, asdict, field

import yaml
from dacite import from_dict

logger = logging.getLogger()


@dataclass
class WorkerSettings:
    log_level: str = "info"
    debug: bool = False


@dataclass
class DatabaseSettings:
    connection_string: str
    pool_min_size: int = 5
    pool_max_size: int = 10
    max_queries: int = 100000


@dataclass
class TopicSettings:
    topic: str
    group_id: str
    service_name: str


@dataclass
class KafkaSettings:
    enabled: bool = True
    brokers: list[str] = field(default_factory=list["localhost:9292"])
    heartbeat: int = 60

    def to_dict(self):
        return asdict(self)


@dataclass
class Settings:
    worker: WorkerSettings
    database: DatabaseSettings
    kafka: KafkaSettings
    parser: TopicSettings
    sender: TopicSettings


def load(path):
    with open(path) as stream:
        data = yaml.load(stream, Loader=yaml.FullLoader)
        settings = from_dict(data_class=Settings, data=data)

        return settings


def dump_settings(settings: Settings):
    return yaml.dump(asdict(settings))
