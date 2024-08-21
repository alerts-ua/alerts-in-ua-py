from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator
from typing_extensions import TypedDict, NamedTuple, Tuple, List, Iterator, Optional, Unpack, Any, Union

from alerts_in_ua.alert import AlertDetails, AlertDetailsDict, AirRaidStatus
from alerts_in_ua.location_resolver import AIR_RAID_STATE_LOCATIONS_ORDERED, resolve_uid
from alerts_in_ua.ua_date_parser import parse_ua_date, ALERTS_META_DATE_TIME_FORMAT


class HistoryPeriod(str, Enum):
    DAY_AGO = 'week_ago'
    WEEK_AGO = 'week_ago'
    MONTH_AGO = 'month_ago'

    def __str__(self) -> str:
        return self.value


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


__all__ = (
    'HistoryPeriod',
    'FilterCriterion',
    'FilterType',
    'AlertsMetaDict',
    'AlertsDataDict',
    'AlertsMeta',
    'Alerts',
    'AirRaidOblastStatusDict',
    'AirRaidOblastStatus',
    'AirRaidOblastStatuses',
)
