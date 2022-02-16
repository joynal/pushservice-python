from enum import Enum


class StatusEnum(Enum):
    queued = "QUEUED"
    running = "RUNNING"
    succeeded = "SUCCEEDED"
    failed = "FAILED"
    canceled = "CANCELED"
