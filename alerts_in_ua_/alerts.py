from datetime import datetime

from pydantic import BaseModel, field_validator
from typing_extensions import TypedDict, NamedTuple, Tuple, List, Iterator, Optional, Unpack, Any, Union

from alerts_in_ua_.alert import AlertDetails, AlertDetailsDict, AirRaidStatus
from alerts_in_ua_.errors import deprecation_warning
from alerts_in_ua_.location_resolver import AIR_RAID_STATE_LOCATIONS_ORDERED, resolve_uid
from alerts_in_ua_.ua_date_parser import parse_ua_date, ALERTS_META_DATE_TIME_FORMAT


class FilterCriterion(NamedTuple):
    field: str
    value: Any


FilterType = Union[
    FilterCriterion,
    Tuple[str, Any]
]


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


# FIXME: remove deprecated Alerts methods
_filter_deprecation_warning_message = """
    This method is possibly an overhead,
    because the new implementation of `Alerts.filter` method 
    allows usage of multiple criteria in a same time, 
    so use Alerts.filter(*criteria: FilterType) instead
"""

_getter_deprecation_warning_message = """
    Since `Alerts` is inherited from `pydantic.BaseModel` and frozen,
    use direct access to `Alerts` instance attributes
"""


class Alerts(BaseModel, frozen=True):
    meta: Optional[AlertsMeta] = None
    alerts: Optional[List[AlertDetails]] = None
    disclaimer: Optional[str] = None

    def __init__(self, /, **data: Unpack[AlertsDataDict]):
        super().__init__(**data)

    @field_validator('meta', mode='before')
    @classmethod
    def parse_meta(cls, value: Any) -> Optional[AlertsMeta]:
        if isinstance(value, dict):
            return AlertsMeta(**value)
        return AlertsMeta(**AlertsMetaDict())

    @field_validator('alerts', mode='before')
    @classmethod
    def parse_alerts(cls, value: Any) -> Optional[List[AlertDetails]]:
        if isinstance(value, list):
            return [AlertDetails(**alert) for alert in value]
        return []

    def __len__(self) -> int:
        if not self.alerts:
            return 0
        return len(self.alerts)

    def __getitem__(self, item: int) -> Optional[AlertDetails]:
        if not self.alerts:
            return None
        return self.alerts[item]

    @property
    def last_updated_at(self) -> Optional[datetime]:
        """
        :return: Last updated time
        """

        return self.meta.last_updated_at if self.meta else None

    def iter_alerts(self) -> Iterator[AlertDetails]:
        """Iterate over all alerts_details"""

        return iter(self.alerts or [])

    def filter(self, *criteria: FilterType) -> List[AlertDetails]:
        """
        Multi-criteria filter
        :param criteria: multiple criteria to filter
        :return: list of unique filtered alerts

        Usage:
            filtered_alerts = self.alerts_details.filter(
                FilterCriterion('location_uid', 16),  # as FilterCriterion
                ('location_type', LocationType.OBLAST), # as Tuple[str, Any]
                ('location_type', 'oblast')
            )
        """

        if not self.alerts or not criteria:
            return []
        filtered_alerts = []
        for criterion in criteria:
            field, value = criterion
            # collect filtered allerts
            filtered_alerts += [
                alert for alert in self.alerts if (
                        hasattr(alert, field) and getattr(alert, field) == value
                )
            ]
        # return list of unique alerts_details
        return list(set(filtered_alerts))

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_oblast_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('oblast')

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_raion_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('raion')

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_hromada_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('hromada')

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_city_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('city')

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_alerts_by_alert_type(self, alert_type: str) -> List[AlertDetails]:
        return self.filter(('alert_type', alert_type))

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_alerts_by_location_title(self, location_title: str) -> List[AlertDetails]:
        return self.filter(('location_title', location_title))

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_alerts_by_location_type(self, location_type: str) -> List[AlertDetails]:
        return self.filter(('location_type', location_type))

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_alerts_by_oblast(self, oblast_title: str) -> List[AlertDetails]:
        return self.filter(('location_oblast', oblast_title))

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_alerts_by_oblast_uid(self, oblast_uid: str) -> List[AlertDetails]:
        return self.filter(('location_oblast_uid', oblast_uid))

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_alerts_by_location_uid(self, location_uid: str) -> List[AlertDetails]:
        return self.filter(('location_uid', location_uid))

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_air_raid_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('air_raid')

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_artillery_shelling_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('artillery_shelling')

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_urban_fights_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('urban_fights')

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_nuclear_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('nuclear')

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_chemical_alerts(self) -> List[AlertDetails]:
        return self.get_alerts_by_alert_type('chemical')

    @deprecation_warning(_getter_deprecation_warning_message)
    def get_all_alerts(self) -> Optional[List[AlertDetails]]:
        """FIXME: This function is deprecated in favor of direct access to the property"""
        return self.alerts

    @deprecation_warning(_getter_deprecation_warning_message)
    def get_last_updated_at(self) -> Optional[datetime]:
        """FIXME: This function is deprecated in favor of direct access to the property"""
        return self.last_updated_at

    @deprecation_warning(_getter_deprecation_warning_message)
    def get_disclaimer(self) -> Optional[str]:
        """FIXME: This function is deprecated in favor of direct access to the property"""
        return self.disclaimer


class AirRaidOblastStatusDict(TypedDict, total=False):
    location_title: str
    location_uid: int
    status: str


class AirRaidOblastStatus(BaseModel, frozen=True):
    location_title: Optional[str] = None
    location_uid: Optional[int] = None
    status: Optional[AirRaidStatus] = None

    def __init__(self, **data: Unpack[AirRaidOblastStatusDict]):
        super().__init__(**data)

    def __str__(self) -> str:
        if self.status == AirRaidStatus.ACTIVE:
            return f"🔴 {self.location_title}"
        elif self.status == AirRaidStatus.PARTLY:
            return f"🟡 {self.location_title}"
        elif self.status == AirRaidStatus.NO_ALERT:
            return f"🟢 {self.location_title}"
        else:
            return f"🟣 {self.location_title}"

    @field_validator('status', mode='before')
    @classmethod
    def parse_status(cls, value: Any) -> Optional[AirRaidStatus]:
        if isinstance(value, str):
            return (AirRaidStatus(value)
                    if value in AirRaidStatus.__members__.values()
                    else AirRaidStatus.UNKNOWN)
        return value

    @deprecation_warning("This function is deprecated in favor of using attribute directly")
    def is_active_on_all_oblast(self) -> bool:
        return self.status == "active"

    @deprecation_warning("This function is deprecated in favor of using attribute directly")
    def is_partly_active(self) -> bool:
        return self.status == "partly"

    @deprecation_warning("This function is deprecated in favor of using attribute directly")
    def is_no_alert(self) -> bool:
        return self.status == "no_alert"


class AirRaidOblastStatuses(list):

    def __init__(self, data: str):
        if not isinstance(data, str):
            raise TypeError(f"Invalid data type, expected str, got {type(data)}")
        if not len(data) == len(AIR_RAID_STATE_LOCATIONS_ORDERED):
            raise ValueError(
                f"Arguments count mismatch, "
                f"expected {len(AIR_RAID_STATE_LOCATIONS_ORDERED)}, "
                f"got {len(data)}")

        statuses = []
        for index, _status in enumerate(data):
            location_title = AIR_RAID_STATE_LOCATIONS_ORDERED[index]
            status = AirRaidOblastStatus(
                location_title=location_title,
                location_uid=resolve_uid(location_title),
                status=_status
            )
            statuses.append(status)

        super().__init__(statuses)

    def __str__(self):
        return "\n".join(str(i) for i in self.__iter__())

    def filter(self, *criteria: FilterType) -> List[AirRaidOblastStatus]:
        """
        Multi-criteria filter
        :param criteria: multiple criteria to filter
        :return: list of unique filtered AirRaidOblastStatus
        """

        if not criteria:
            return []
        filtered_alerts = []
        for criterion in criteria:
            field, value = criterion
            # collect filtered allerts
            filtered_alerts += [
                alert for alert in self if (
                        hasattr(alert, field) and getattr(alert, field) == value
                )
            ]
        # return list of unique air raid statuses
        return list(set(filtered_alerts))

    @deprecation_warning(_filter_deprecation_warning_message)
    def filter_by_status(self, status: AirRaidStatus):
        return self.filter(('status', status))

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_active_alert_oblasts(self) -> List[AirRaidOblastStatus]:
        return self.filter(('status', AirRaidStatus.ACTIVE))

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_partly_active_alert_oblasts(self) -> List[AirRaidOblastStatus]:
        return self.filter(('status', AirRaidStatus.PARTLY))

    @deprecation_warning(_filter_deprecation_warning_message)
    def get_no_alert_oblasts(self) -> List[AirRaidOblastStatus]:
        return self.filter(('status', AirRaidStatus.NO_ALERT))


__all__ = (
    'FilterCriterion',
    'FilterType',
    'AlertsMetaDict',
    'AlertsDataDict',
    'AlertsMeta',
    'Alerts',
    'AirRaidOblastStatusDict',
    'AirRaidOblastStatus',
    'AirRaidOblastStatuses'
)
