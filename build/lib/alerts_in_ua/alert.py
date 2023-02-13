from typing import Optional, Dict, List, Union
import json
import datetime
import pytz
from .ua_date_parser import UaDateParser

class Alert:

    def __init__(self, data: Dict):
        self.id = data["id"]
        self.location_title = data.get("location_title")
        self.location_type = data.get("location_type")
        self.started_at = UaDateParser.parse_date(data.get("started_at"))
        self.finished_at = UaDateParser.parse_date(data.get("finished_at"))
        self.updated_at = UaDateParser.parse_date(data.get("updated_at"))
        self.alert_type = data.get("alert_type")
        self.location_uid = data.get("location_uid")
        self.location_oblast = data.get("location_oblast")
        self.location_raion = data.get("location_raion")
        self.notes = data.get("notes")
        self.calculated = data.get("calculated")


    def is_finished(self) -> bool:
        return self.finished_at is not None
    def __repr__(self):
        return f"Alert({{'id': {self.id!r}, 'location_title': {self.location_title!r}, 'location_type': {self.location_type!r}, 'started_at': {self.started_at!r}, 'finished_at': {self.finished_at!r}, 'updated_at': {self.updated_at!r}, 'alert_type': {self.alert_type!r}, 'location_uid': {self.location_uid!r}, 'location_oblast': {self.location_oblast!r}, 'location_raion': {self.location_raion!r}, 'notes': {self.notes!r}, 'calculated': {self.calculated!r}}}"