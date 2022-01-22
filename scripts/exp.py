from uuid import UUID

import dacite
from dacite import from_dict

from parser.core.domain.entities import Push

data = {
    "id": "ea7c9b876e4e466a87fabeb9177fb770",
    "site_id": "d20b9968eb804454a2aa3ca188d690b5",
    "title": "I came from demo",
    "status": "RUNNING",
    "launch_url": "https://joynal.dev",
    "priority": "normal",
    "time_to_live": 259200,
    "options": {
        "body": "Ignore it, it's a test push",
        "icon": "https://avatars3.githubusercontent.com/u/6458212",
    },
}

push = from_dict(
    data_class=Push,
    data=data,
    config=dacite.Config(cast=[UUID]),
)

print(push)
