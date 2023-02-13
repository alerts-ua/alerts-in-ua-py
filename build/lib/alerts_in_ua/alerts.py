from .alert import Alert
from typing import Optional, Dict, List, Union
from .ua_date_parser import UaDateParser
import datetime
import pytz

class Alerts:
    def __init__(self, data: Dict):
        self.alerts = [Alert(alert) for alert in data.get('alerts')]
        meta = data.get('meta')
        self.last_updated_at = UaDateParser.parse_date(meta.get('last_updated_at'),"%Y/%m/%d %H:%M:%S %z")
        self.disclaimer = data.get('disclaimer')

    def filter(self, *args: str) -> List[Alert]:
        filtered_alerts = self.alerts
        for i in range(0, len(args), 2):
            filtered_alerts = [alert for alert in filtered_alerts if getattr(alert, args[i]) == args[i + 1]]
        return filtered_alerts

    def get_oblast_alerts(self) -> List[Alert]:
        return self.get_alerts_by_alert_type('oblast')

    def get_raion_alerts(self) -> List[Alert]:
        return self.get_alerts_by_alert_type('raion')

    def get_hromada_alerts(self) -> List[Alert]:
        return self.get_alerts_by_alert_type('hromada')

    def get_city_alerts(self) -> List[Alert]:
        return self.get_alerts_by_alert_type('city')

    def get_alerts_by_alert_type(self, alert_type: str) -> List[Alert]:
        return self.filter('alert_type',alert_type)

    def get_alerts_by_location_title(self, location_title: str) -> List[Alert]:
        return self.filter('location_title',location_title)

    def get_alerts_by_location_type(self, location_type: str) -> List[Alert]:
        return self.filter('location_type',location_type)

    def get_alerts_by_oblast(self, oblast_title: str) -> List[Alert]:
        return self.filter('location_oblast',oblast_title)

    def get_alerts_by_location_uid(self, location_uid: str) -> List[Alert]:
        return self.filter('location_uid',location_uid)

    def get_air_raid_alerts(self) -> List[Alert]:
        return self.get_alerts_by_alert_type('air_raid')

    def get_artillery_shelling_alerts(self) -> List[Alert]:
        return self.get_alerts_by_alert_type('artillery_shelling')

    def get_urban_fights_alerts(self) -> List[Alert]:
        return self.get_alerts_by_alert_type('urban_fights')

    def get_nuclear_alerts(self) -> List[Alert]:
        return self.get_alerts_by_alert_type('nuclear')

    def get_chemical_alerts(self) -> List[Alert]:
        return self.get_alerts_by_alert_type('chemical')

    def get_all_alerts(self) -> List[Alert]:
        return self.alerts

    def get_last_updated_at(self) -> datetime.datetime:
        return self.last_updated_at

    def get_disclaimer(self) -> str:
        return self.disclaimer

    def __iter__(self) -> List[Alert]:
        return iter(self.alerts)

    def __repr__(self) -> str:
        return str(self.alerts)