from typing import Optional, Dict, List, Union
import json
import datetime
import pytz

kyiv_tz = pytz.timezone('Europe/Kyiv')

class Alert:

    def __init__(self, data: Dict):
        self.id = data["id"]
        self.location_title = data.get("location_title")
        self.location_type = data.get("location_type")
        self.started_at = self.parse_date(data.get("started_at"))
        self.finished_at = self.parse_date(data.get("finished_at"))
        self.updated_at = self.parse_date(data.get("updated_at"))
        self.alert_type = data.get("alert_type")
        self.location_uid = data.get("location_uid")
        self.location_oblast = data.get("location_oblast")
        self.location_raion = data.get("location_raion")
        self.notes = data.get("notes")
        self.calculated = data.get("calculated")

    @staticmethod
    def parse_date(date_string: Optional[str]) -> Optional[datetime.datetime]:
        if date_string:
            utc_dt = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
            local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(kyiv_tz)
            return kyiv_tz.normalize(local_dt)

        return None

    def is_finished(self) -> bool:
        return self.finished_at is not None