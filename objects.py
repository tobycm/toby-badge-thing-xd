from typing import Literal


class Data:
    def __init__(self, raw_json: dict) -> None:
        self.avatar_url = raw_json["avatar_url"]
        self.name = raw_json["name"]
        self.status = raw_json["status"]

    avatar_url: str
    name: str
    status: Literal["online", "offline", "idle", "dnd"]
