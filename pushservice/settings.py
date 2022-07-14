import logging
from abc import ABC
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field

import yaml
from dacite import from_dict

logger = logging.getLogger()


class BaseSettings(ABC):
    def display(self) -> [str]:
        settings = vars(self)

        fields = []

        for key in settings:
            if issubclass(type(settings[key]), BaseSettings):
                sub_fields = settings[key].display()
                for field in sub_fields:
                    fields.append(f"{key} | {field}")
            else:
                if key in self._sensitive_fields():
                    masked_field = self._mask(key, settings[key])
                    fields.append(f"{key}={masked_field}")
                else:
                    fields.append(f"{key}={settings[key]}")

        return fields

    @staticmethod
    def _sensitive_fields() -> [str]:
        """
        The field name of any sensitive values should go here, so they get masked
        """
        return ["password", "api_key"]

    @staticmethod
    def _mask(name, val) -> str:
        unmask_len = 2
        min_length = 8

        if len(val) < min_length:
            raise Exception(
                f"The sensitive setting '{name}' "
                f"must be at least {min_length} characters"
            )

        masked = (len(val) - unmask_len) * "#"
        unmasked = val[-unmask_len:]
        return masked + unmasked


@dataclass(frozen=True)
class MonitorSettings(BaseSettings):
    log_level: str = "info"
    debug: bool = False
    local_development: bool = False


@dataclass(frozen=True)
class WebApiSettings(BaseSettings):
    host: str = "localhost"
    port: int = 8080
    enabled: bool = True


@dataclass(frozen=True)
class DatabaseSettings(BaseSettings):
    connection_string: str
    pool_min_size: int = 5
    pool_max_size: int = 10
    max_queries: int = 100000


@dataclass(frozen=True)
class TopicSettings(BaseSettings):
    topic: str
    group_id: str


@dataclass(frozen=True)
class KafkaSettings(BaseSettings):
    enabled: bool = True
    brokers: list[str] = field(default_factory=lambda: ["localhost:9292"])
    heartbeat: int = 60


@dataclass(frozen=True)
class Settings(BaseSettings):
    web_api: WebApiSettings
    database: DatabaseSettings
    kafka: KafkaSettings
    parser: TopicSettings
    sender: TopicSettings
    monitor: MonitorSettings = MonitorSettings()


def _read_file(path: str) -> str:
    with open(path) as f:
        return f.read()


def _parse_yaml(content: str) -> dict:
    return yaml.load(content, Loader=yaml.FullLoader)


def settings_from_dict(content: dict) -> Settings:
    return from_dict(Settings, data=content)


def load_settings(path_to_settings: str) -> Settings:
    try:
        c = _read_file(path_to_settings)
        d = _parse_yaml(c)
        settings = settings_from_dict(d)

        return settings
    except (TypeError, FileNotFoundError):
        return from_dict(Settings, data=dict())


def dump_settings(settings: Settings):
    return yaml.dump(asdict(settings))
