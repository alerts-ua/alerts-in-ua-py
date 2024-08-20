import datetime
import pytz
from typing_extensions import Optional

ALERT_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
ALERTS_META_DATE_TIME_FORMAT = "%Y/%m/%d %H:%M:%S %z"

def parse_ua_date(date_string: Optional[str],
                  time_format: str = ALERT_DATE_TIME_FORMAT) -> Optional[datetime.datetime]:
    if date_string:
        if 'Europe/Kyiv' in pytz.all_timezones_set:
            kyiv_tz = pytz.timezone('Europe/Kyiv')
        # KyivNotKiev. Hopefully remove this tz_code in future
        elif 'Europe/Kiev' in pytz.all_timezones_set:
            kyiv_tz = pytz.timezone('Europe/Kiev')
        else:
            return None
        utc_dt = datetime.datetime.strptime(date_string, time_format)
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(kyiv_tz)
        return kyiv_tz.normalize(local_dt)
    return None


__all__ = (
    'parse_ua_date',
    'ALERT_DATE_TIME_FORMAT',
    'ALERTS_META_DATE_TIME_FORMAT'
)
