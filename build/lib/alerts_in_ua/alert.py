from typing import Optional, Dict, List, Union
import json
class Alert:

    def __init__(self, data: Dict):
        self.id = data["id"]
        self.location_title = data["location_title"]
        self.location_type = data["location_type"]
        self.started_at = data["started_at"]
        self.finished_at = data["finished_at"]
        self.updated_at = data["updated_at"]
        self.alert_type = data["alert_type"]
        self.location_uid = data["location_uid"]
        self.location_oblast = data["location_oblast"]
        self.location_raion = data.get("location_raion")
        self.notes = data.get("notes")
        self.calculated = data["calculated"]

    def is_finished(self) -> bool:
        return self.finished_at is not None
    def __repr__(self):
       return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii=False)
