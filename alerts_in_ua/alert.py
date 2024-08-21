from datetime import datetime, timedelta
from enum import Enum

from pydantic import BaseModel, field_validator
from typing_extensions import Optional, TypedDict, Unpack, Any

from alerts_in_ua.ua_date_parser import parse_ua_date, ALERT_DATE_TIME_FORMAT


class LocationType(str, Enum):
    OBLAST = 'oblast'
    RAION = 'raion'
    CITY = 'city'
    HROMADA = 'hromada'
    UNKNOWN = 'unknown'

    def __str__(self) -> str:
        return self.value


class AlertType(str, Enum):
    AIR_RAID = 'air_raid'
    ARTILLERY_SHELLING = 'artillery_shelling'
    URBAN_FIGHTS = 'urban_fights'
    CHEMICAL = 'chemical'
    NUCLEAR = 'nuclear'
    UNKNOWN = 'unknown'

    def __str__(self) -> str:
        return self.value


class AirRaidStatus(str, Enum):
    ACTIVE = 'A'
    PARTLY = 'P'
    NO_ALERT = 'N'
    UNKNOWN = 'unknown'

    def __str__(self) -> str:
        return self.value


class AlertDetailsDict(TypedDict, total=False):
    """Alert Details Response Typing Annotation"""

    id: int
    location_title: str
    location_type: str
    started_at: Optional[str]
    finished_at: Optional[str]
    updated_at: Optional[str]
    alert_type: str
    location_uid: str
    location_oblast: str
    location_oblast_uid: str
    location_raion: str
    notes: Optional[str]
    calculated: bool


class AlertDetails(BaseModel, frozen=True):
    """
    Represents an alert in the location

    # Usage:
    alert = AlertDetails(
        **{
            "id": 10,
            "location_title": "Луганська область",
            "location_type": "oblast",
            "started_at": "2022-04-04T16:45:39.000Z",
            "finished_at": None,
            "updated_at": "2022-04-08T08:04:26.316Z",
            "alert_type": "air_raid",
            "location_uid": "16",
            "location_oblast": "Луганська область",
            "location_oblast_uid": "16",
            "location_raion": "Луганський район",
            "notes": "За повідомленям голови ОВА",
            "calculated": False
        }
    )
    print(a)
    """

    id: Optional[int] = None
    location_title: Optional[str] = "unknown"
    location_type: LocationType = LocationType.UNKNOWN
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    alert_type: AlertType = AlertType.UNKNOWN
    location_uid: Optional[int] = None
    location_oblast: Optional[str] = "unknown"
    location_oblast_uid: Optional[int] = None
    location_raion: Optional[str] = "unknown"
    calculated: Optional[bool] = None
    notes: Optional[str] = ""

    def __init__(self, /, **data: Unpack[AlertDetailsDict]):
        super().__init__(**data)

    def __str__(self) -> str:
        attrs = ', '.join([f"{k}={v}" for k, v in self.__dict__.items()])
        return f"A({attrs})"

    @property
    def is_finished(self) -> bool:
        return self.finished_at is not None

    @property
    def duration(self) -> Optional[timedelta]:
        if self.started_at:
            if self.finished_at:
                return self.finished_at - self.started_at
            else:
                if now_datetime := parse_ua_date(
                        datetime.now().strftime(ALERT_DATE_TIME_FORMAT)):
                    return now_datetime - self.started_at
        return None

    @field_validator('started_at', 'finished_at', 'updated_at', mode='before')
    @classmethod
    def parse_datetime(cls, value: Any) -> Optional[datetime]:
        if isinstance(value, str):
            return parse_ua_date(value)
        return value

    @field_validator('location_type', mode='before')
    @classmethod
    def parse_location_type(cls, value: Any) -> Optional[LocationType]:
        if isinstance(value, str):
            return (LocationType(value)
                    if value in LocationType.__members__.values()
                    else LocationType.UNKNOWN)
        return value

    @field_validator('alert_type', mode='before')
    @classmethod
    def parse_alert_type(cls, value: Any) -> Optional[AlertType]:
        if isinstance(value, str):
            return (AlertType(value)
                    if value in AlertType.__members__.values()
                    else AlertType.UNKNOWN)
        return value


__all__ = (
    'AlertType',
    'LocationType',
    'AirRaidStatus',
    'AlertDetailsDict',
    'AlertDetails',
)
