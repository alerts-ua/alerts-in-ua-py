from typing import Optional, Dict, List, Union
import json
import datetime
import pytz
from .ua_date_parser import UaDateParser
from .threat import Threat

class Alert:

    def __init__(self, data: Dict):
        self.id = data["id"]
        self.location_title = data.get("location_title")
        self.location_title_en = data.get("location_title_en")
        self.location_type = data.get("location_type")
        self.started_at = UaDateParser.parse_date(data.get("started_at"))
        self.finished_at = UaDateParser.parse_date(data.get("finished_at"))
        self.updated_at = UaDateParser.parse_date(data.get("updated_at"))
        self.alert_type = data.get("alert_type")
        self.location_uid = data.get("location_uid")
        self.location_oblast = data.get("location_oblast")
        self.location_oblast_uid = data.get("location_oblast_uid")
        self.location_raion = data.get("location_raion")
        self.notes = data.get("notes")
        self.country = data.get("country")
        self.calculated = data.get("calculated")
        self.alert_level = data.get("alert_level")
        self.threats = [Threat(threat) for threat in data.get("threats") or []]


    def is_finished(self) -> bool:
        return self.finished_at is not None

    def is_red(self) -> bool:
        return self.alert_level == "red"

    def is_yellow(self) -> bool:
        return self.alert_level == "yellow"

    def has_threats(self) -> bool:
        return len(self.threats) > 0

    def get_threats_by_type(self, threat_type: str) -> List[Threat]:
        return [threat for threat in self.threats if threat.threat_type == threat_type]

    def __repr__(self):
        return f"Alert({{'id': {self.id!r}, 'location_title': {self.location_title!r}, 'location_title_en': {self.location_title_en!r}, 'location_type': {self.location_type!r}, 'started_at': {self.started_at!r}, 'finished_at': {self.finished_at!r}, 'updated_at': {self.updated_at!r}, 'alert_type': {self.alert_type!r}, 'location_uid': {self.location_uid!r}, 'location_oblast': {self.location_oblast!r}, 'location_oblast_uid': {self.location_oblast_uid!r}, 'location_raion': {self.location_raion!r}, 'notes': {self.notes!r}, 'country': {self.country!r}, 'calculated': {self.calculated!r}, 'alert_level': {self.alert_level!r}, 'threats': {self.threats!r}}})"