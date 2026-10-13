from typing import Dict
from .ua_date_parser import UaDateParser

class Threat:

    def __init__(self, data: Dict):
        self.threat_type = data.get("threat_type")
        self.level = data.get("level")
        self.started_at = UaDateParser.parse_date(data.get("started_at"))
        self.source_message = data.get("source_message")

    def is_red(self) -> bool:
        return self.level == "red"

    def is_yellow(self) -> bool:
        return self.level == "yellow"

    def __repr__(self):
        return f"Threat({{'threat_type': {self.threat_type!r}, 'level': {self.level!r}, 'started_at': {self.started_at!r}, 'source_message': {self.source_message!r}}})"
