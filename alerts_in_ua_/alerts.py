from datetime import datetime
from typing_extensions import TypedDict, List, Iterator, Optional, Unpack, Union, Any
from pydantic import BaseModel, field_validator
from alerts_in_ua_.ua_date_parser import parse_ua_date, ALERTS_META_DATE_TIME_FORMAT
from alerts_in_ua_.alert import AlertDetails, AlertDetailsDict


class AlertsMetaDict(TypedDict, total=False):
    last_updated_at: Optional[str]
    type: Optional[str]


class AlertsDataDict(TypedDict, total=False):
    alerts: Optional[List[AlertDetailsDict]]
    meta: Optional[AlertsMetaDict]
    disclaimer: Optional[str]


class AlertsMeta(BaseModel, frozen=True):
    last_updated_at: Optional[datetime] = None
    type: Optional[str] = None

    def __init__(self, /, **data: Unpack[AlertsMetaDict]):
        super().__init__(**data)

    @field_validator('last_updated_at', mode='before')
    @classmethod
    def parse_datetime(cls, value) -> Optional[datetime]:
        if isinstance(value, str):
            return parse_ua_date(value, ALERTS_META_DATE_TIME_FORMAT)
        return value


class Alerts(BaseModel, frozen=True):
    meta: Optional[AlertsMeta] = None
    alerts: Optional[List[AlertDetails]] = None
    disclaimer: Optional[str] = None

    def __init__(self, /, **data: Unpack[AlertsDataDict]):
        if not data.get('meta'):
            data['meta'] = AlertsMetaDict()
        if not data.get('alerts'):
            data['alerts'] = []
        super().__init__(**data)

    def __len__(self) -> int:
        if not self.alerts:
            return 0
        return len(self.alerts)

    @property
    def last_updated_at(self) -> Optional[datetime]:
        return self.meta.last_updated_at if self.meta else None

    def iter_alerts(self) -> Iterator[AlertDetails]:
        return iter(self.alerts or [])

    def filter(self, *criteria: Union[str, Any]) -> List[AlertDetails]:
        # FIXME: does not work for multiple criteria, cause of reassignment on each iteration
        if not self.alerts:
            return []
        filtered_alerts = self.alerts
        for i in range(0, len(criteria), 2):
            filtered_alerts = [alert for alert in filtered_alerts if getattr(alert, criteria[i]) == criteria[i + 1]]
        return filtered_alerts

    def get_oblast_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('oblast')

    def get_raion_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('raion')

    def get_hromada_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('hromada')

    def get_city_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('city')

    def get_alerts_by_alert_type(self, alert_type: str) -> List[AlertDetails]:
        return self.filter('alert_type', alert_type)

    def get_alerts_by_location_title(self, location_title: str) -> List[AlertDetails]:
        return self.filter('location_title', location_title)

    def get_alerts_by_location_type(self, location_type: str) -> List[AlertDetails]:
        return self.filter('location_type', location_type)

    def get_alerts_by_oblast(self, oblast_title: str) -> List[AlertDetails]:
        return self.filter('location_oblast', oblast_title)

    def get_alerts_by_oblast_uid(self, oblast_uid: str) -> List[AlertDetails]:
        return self.filter('location_oblast_uid', oblast_uid)

    def get_alerts_by_location_uid(self, location_uid: str) -> List[AlertDetails]:
        return self.filter('location_uid', location_uid)

    def get_air_raid_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('air_raid')

    def get_artillery_shelling_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('artillery_shelling')

    def get_urban_fights_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('urban_fights')

    def get_nuclear_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('nuclear')

    def get_chemical_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('chemical')


__all__ = (
    'AlertsMetaDict',
    'AlertsDataDict',
    'AlertsMeta',
    'Alerts'
)
