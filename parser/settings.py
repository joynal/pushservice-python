import logging
import re
from dataclasses import dataclass

import yaml

logger = logging.getLogger()


@dataclass
class Worker:
    log_level: str = "info"
    debug: bool = False


@dataclass
class DatabaseSettings:
    connection_uri: str
    pool_min_size: int = 5
    pool_max_size: int = 10
    max_queries: int = 100000


class Settings:
    def __init__(self, settings):
        self.app = Worker(**settings.get("worker", {}))
        self.database = DatabaseSettings(**settings.get("database", {}))

    def dump(self):
        def _log(key, value, section):
            class_dict = getattr(value, "__dict__", None)

            if isinstance(value, dict):
                for v in value:
                    _log(v, value[v], f"{section}|{key}")
            elif class_dict:
                for item in class_dict:
                    value = getattr(class_dict, item, None)
                    _log(item, value, f"{section}|{key}")
            else:
                # If it's the database section
                if re.search(r"^database", section):
                    # Let's mask user and password for database connections'
                    if isinstance(value, str):
                        match = re.search(r"://(.+)?@", value)
                        if match:
                            value = value.replace(match[1], "######")
                logger.info(f"{section} | {key} = {value}")

        logger.info("CURRENT WORKER SETTINGS | START")
        for setting in self.__dict__:
            config = getattr(self, setting, None)

            for key in config.__dict__:
                value = getattr(config, key, None)
                _log(key, value, setting)
        logger.info("CURRENT WORKER SETTINGS | END")


def load_settings(path):
    with open(path) as stream:
        return Settings(yaml.safe_load(stream))
