import aiohttp
from .errors import UnauthorizedError, RateLimitError, InternalServerError, ForbiddenError, ApiError,InvalidParameterException
from .alert import Alert
from .alerts import Alerts
from .user_agent import UserAgent
from .air_raid_alert_oblast_statuses import AirRaidAlertOblastStatuses
from .air_raid_alert_oblast_status import AirRaidAlertOblastStatus
from .air_raid_alert_status import AirRaidAlertStatus
from .air_raid_alert_statuses import AirRaidAlertStatuses
from typing import List, Dict, Union
from .location_uid_resolver import LocationUidResolver
from .air_raid_alert_status_resolver import AirRaidAlertStatusResolver
class AsyncClient:
    REQUEST_TIMEOUT = 5
    API_BASE_URL = "https://api.alerts.in.ua"

    def __init__(self, token: str):
        self.token = token
        self.base_url = "/v1/"
        self.location_uid_resolver = LocationUidResolver()

        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": UserAgent.get_user_agent(self.token)
        }
        self.cache = {}

    async def _request(self, endpoint: str, use_cache=True):
        async with aiohttp.ClientSession(AsyncClient.API_BASE_URL) as session:
            # Check if endpoint is in cache and return cached data if not modified
            if endpoint in self.cache and use_cache == True:
                cached_data = self.cache[endpoint]
                headers = {
                    **self.headers,
                    **{"If-Modified-Since": cached_data["Last-Modified"]},
                }
                response = await session.get(
                    self.base_url + endpoint,
                    headers=headers,
                    timeout=AsyncClient.REQUEST_TIMEOUT,
                )
                if response.status == 304:
                    return cached_data["Data"]

            # Make the request
            response = await session.get(
                self.base_url + endpoint,
                headers=self.headers,
                timeout=AsyncClient.REQUEST_TIMEOUT,
            )

            # Check if response is successful
            if response.status == 200:
                data = await response.json()
                self.cache[endpoint] = {
                    "Data": data,
                    "Last-Modified": response.headers["Last-Modified"],
                }
                return data
            else:
                message = None
                try:
                    data = await response.json()
                    json_message = data.get("message")
                    message = f"{json_message} HTTP Code:{response.status}"
                except:
                    pass
                if response.status == 401:
                    if message is None:
                        message = "Unauthorized: Incorrect token"
                    raise UnauthorizedError(message)
                elif response.status == 403:
                    if message is None:
                        message = "Forbidden. API may not be available in some regions. Please ask api@alerts.in.ua for details."
                    raise ForbiddenError(message)
                elif response.status == 429:
                    if message is None:
                        message = "Too many requests: Rate limit exceeded"
                    raise RateLimitError(message)
                elif response.status == 500:
                    raise InternalServerError("Internal server error")
                else:
                    raise ApiError(f"Unknown error. HTTP Code:{response.status}")

    async def get_active_alerts(self, use_cache=True) -> Alerts:
        data = await self._request("alerts/active.json", use_cache=use_cache)
        return Alerts(data)

    async def get_alerts_history(self, oblast_uid_or_location_title: Union[int, str], period: str = 'month_ago', use_cache: bool = True) -> Alerts:
        if isinstance(oblast_uid_or_location_title, str):
           if oblast_uid_or_location_title.isdigit():
              oblast_uid = int(oblast_uid_or_location_title)
           else:
              oblast_uid = self.location_uid_resolver.resolve_uid(oblast_uid_or_location_title)
        else:
            oblast_uid = oblast_uid_or_location_title
        url = f"regions/{oblast_uid}/alerts/{period}.json"
        data = await self._request(url, use_cache=use_cache)
        return Alerts(data)


    async def get_air_raid_alert_status(self, oblast_uid_or_location_title: Union[int, str], oblast_level_only=False, use_cache=True) -> AirRaidAlertOblastStatus:
        if isinstance(oblast_uid_or_location_title, str):
           if oblast_uid_or_location_title.isdigit():
              oblast_uid = int(oblast_uid_or_location_title)
           else:
              oblast_uid = self.location_uid_resolver.resolve_uid(oblast_uid_or_location_title)
        else:
            oblast_uid = oblast_uid_or_location_title
        data = await self._request(f"iot/active_air_raid_alerts/{oblast_uid}.json", use_cache=use_cache)
        return AirRaidAlertOblastStatus(location_title = self.location_uid_resolver.resolve_location_title(oblast_uid),status=data,oblast_level_only=oblast_level_only)

    async def get_air_raid_alert_statuses_by_oblast(self, oblast_level_only=False, use_cache=True) -> AirRaidAlertOblastStatuses:
        data = await self._request("iot/active_air_raid_alerts_by_oblast.json", use_cache=use_cache)
        return AirRaidAlertOblastStatuses(data,oblast_level_only=oblast_level_only)

    async def get_air_raid_alert_statuses(self, use_cache=True) -> AirRaidAlertStatuses:

        data = await self._request("iot/active_air_raid_alerts.json", use_cache=use_cache)
        
        status_string = data if isinstance(data, str) else str(data)
        
        resolved_statuses = AirRaidAlertStatusResolver.resolve_status_string(
            status_string, 
            self.location_uid_resolver.uid_to_location
        )
        
        statuses = []
        for resolved_status in resolved_statuses:
            air_raid_status = AirRaidAlertStatus(
                location_title=resolved_status['location_title'],
                status=resolved_status['status'],
                uid=resolved_status['uid']
            )
            statuses.append(air_raid_status)
                
        return AirRaidAlertStatuses(statuses)