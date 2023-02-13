import datetime
import pytz
from typing import Optional

class UaDateParser:
    @staticmethod
    def parse_date(date_string: Optional[str], time_format: str='%Y-%m-%dT%H:%M:%S.%fZ' ) -> Optional[datetime.datetime]:
        if date_string:
            kyiv_tz = None
            try:
                kyiv_tz = pytz.timezone('Europe/Kyiv')
            except pytz.UnknownTimeZoneError:
                kyiv_tz = pytz.timezone('Europe/Kiev') # KyivNotKiev. Hopefully remove this method in future

            utc_dt = datetime.datetime.strptime(date_string, time_format)
            local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(kyiv_tz)
            return kyiv_tz.normalize(local_dt)
        return None

