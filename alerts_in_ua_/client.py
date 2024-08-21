import os

import aiohttp
import requests
from aiohttp import ClientTimeout
from typing_extensions import Optional, Any, Dict, Union

from alerts_in_ua_.alerts import Alerts, HistoryPeriod, AirRaidOblastStatus, AirRaidOblastStatuses
from alerts_in_ua_.errors import (ApiError, RateLimitError,
                                  ForbiddenError, UnauthorizedError, InternalServerError)
from alerts_in_ua_.location_resolver import resolve_uid, resolve_title
from alerts_in_ua_.user_agent import USER_AGENT

REQUEST_TIMEOUT = 5
API_BASE_URL = "https://api.alerts.in.ua"


class Client:
    def __init__(self, token: Optional[str] = None):
        self.token = self._check_token(token)
        self.base_url = API_BASE_URL + "/v1/"
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": USER_AGENT
        }
        self.cache: Dict[str, Any] = {}

    @staticmethod
    def _check_token(token: Optional[str] = None) -> str:
        if not token:
            if 'AIU_API_TOKEN' in os.environ:
                return os.environ['AIU_API_TOKEN']
            raise EnvironmentError(
                "API token not provided. Please put `token` to Client constructor "
                "or set it as environment variable `AIU_API_TOKEN`"
            )
        return token

    def _request(self, endpoint: str, use_cache: bool = True) -> Any:
        # Check if endpoint is in cache and return cached data if not modified
        if use_cache and self.cache.get(endpoint):
            cached_data = self.cache[endpoint]
            headers = {
                **self.headers,
                **{"If-Modified-Since": cached_data["Last-Modified"]},
            }
            response = requests.get(
                self.base_url + endpoint,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )
            if response.status_code == 304:
                return cached_data["Data"]

        # Make the request
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            timeout=REQUEST_TIMEOUT,
        )

        # Check if response is successful
        status_code = response.status_code
        if status_code == 200:
            data = response.json()
            self.cache[endpoint] = {
                "Data": data,
                "Last-Modified": response.headers["Last-Modified"],
            }
            return data
        message = None
        try:
            data = response.json()  # can raise requests.exceptions.JSONDecodeError
            json_message = data.get("message")
            message = f"{json_message} HTTP Code: {status_code}"
        finally:
            self._process_exception(status_code, message)

    async def _async_request(self, endpoint: str, use_cache: bool = True) -> Any:
        async with aiohttp.ClientSession() as session:
            # Check if endpoint is in cache and return cached data if not modified
            if use_cache and self.cache.get(endpoint):
                cached_data = self.cache[endpoint]
                headers = {
                    **self.headers,
                    **{"If-Modified-Since": cached_data["Last-Modified"]},
                }
                response = await session.get(
                    self.base_url + endpoint,
                    headers=headers,
                    timeout=ClientTimeout(REQUEST_TIMEOUT),
                )
                if response.status == 304:
                    return cached_data["Data"]

            # Make the request
            response = await session.get(
                self.base_url + endpoint,
                headers=self.headers,
                timeout=ClientTimeout(REQUEST_TIMEOUT),
            )

            # Check if response is successful
            status_code = response.status
            if response.status == 200:
                data = await response.json()
                self.cache[endpoint] = {
                    "Data": data,
                    "Last-Modified": response.headers["Last-Modified"],
                }
                return data
            message = None
            try:
                data = await response.json()  # can raise requests.exceptions.JSONDecodeError
                json_message = data.get("message")
                message = f"{json_message} HTTP Code: {status_code}"
            finally:
                self._process_exception(status_code, message)

    @staticmethod
    def _process_exception(status_code, message):
        if status_code == 401:
            raise UnauthorizedError(message)
        elif status_code == 403:
            raise ForbiddenError(message)
        elif status_code == 429:
            raise RateLimitError(message)
        elif status_code == 500:
            raise InternalServerError(message)
        else:
            raise ApiError(f"Unknown error. HTTP Code:{status_code}")

    def get_active(self, use_cache=True) -> Alerts:
        data = self._request("alerts/active.json", use_cache=use_cache)
        return Alerts(**data)

    async def async_get_active(self, use_cache=True) -> Alerts:
        data = await self._async_request("alerts/active.json", use_cache=use_cache)
        return Alerts(**data)

    def get_history(self, oblast_uid_or_location_title: Union[int, str],
                    period: Union[HistoryPeriod, str] = HistoryPeriod.WEEK_AGO,
                    use_cache: bool = True) -> Alerts:
        if isinstance(oblast_uid_or_location_title, str):
            if oblast_uid_or_location_title.isdigit():
                oblast_uid = int(oblast_uid_or_location_title)
            else:
                oblast_uid = resolve_uid(oblast_uid_or_location_title)
        elif isinstance(oblast_uid_or_location_title, int):
            oblast_uid = oblast_uid_or_location_title
        else:
            raise TypeError(f"Expected an int or str, got {type(oblast_uid_or_location_title)}")

        url = f"regions/{oblast_uid}/alerts/{period}.json"
        data = self._request(url, use_cache=use_cache)
        return Alerts(**data)

    async def async_get_history(self, oblast_uid_or_location_title: Union[int, str],
                                period: Union[HistoryPeriod, str] = HistoryPeriod.WEEK_AGO,
                                use_cache: bool = True) -> Alerts:
        if isinstance(oblast_uid_or_location_title, str):
            if oblast_uid_or_location_title.isdigit():
                oblast_uid = int(oblast_uid_or_location_title)
            else:
                oblast_uid = resolve_uid(oblast_uid_or_location_title)
        else:
            oblast_uid = oblast_uid_or_location_title
        url = f"regions/{oblast_uid}/alerts/{period}.json"
        data = await self._async_request(url, use_cache=use_cache)
        return Alerts(**data)

    def get_air_raid(self, oblast_uid_or_location_title: Union[int, str],
                     use_cache=True) -> AirRaidOblastStatus:
        if isinstance(oblast_uid_or_location_title, str):
            if oblast_uid_or_location_title.isdigit():
                oblast_uid = int(oblast_uid_or_location_title)
            else:
                oblast_uid = resolve_uid(oblast_uid_or_location_title)
        else:
            oblast_uid = oblast_uid_or_location_title
        data = self._request(
            f"iot/active_air_raid_alerts/{oblast_uid}.json",
            use_cache=use_cache
        )
        return AirRaidOblastStatus(
            location_title=resolve_title(oblast_uid),
            location_uid=oblast_uid,
            status=data
        )

    async def async_get_air_raid(self, oblast_uid_or_location_title: Union[int, str],
                                 use_cache=True) -> AirRaidOblastStatus:
        if isinstance(oblast_uid_or_location_title, str):
            if oblast_uid_or_location_title.isdigit():
                oblast_uid = int(oblast_uid_or_location_title)
            else:
                oblast_uid = resolve_uid(oblast_uid_or_location_title)
        else:
            oblast_uid = oblast_uid_or_location_title
        data = await self._async_request(
            f"iot/active_air_raid_alerts/{oblast_uid}.json",
            use_cache=use_cache
        )
        return AirRaidOblastStatus(
            location_title=resolve_title(oblast_uid),
            location_uid=oblast_uid,
            status=data
        )

    def get_air_raids(self, use_cache=True) -> AirRaidOblastStatuses:
        data = self._request(
            "iot/active_air_raid_alerts_by_oblast.json",
            use_cache=use_cache
        )
        return AirRaidOblastStatuses(data)

    async def async_get_air_raids(self, use_cache=True) -> AirRaidOblastStatuses:
        data = await self._async_request(
            "iot/active_air_raid_alerts_by_oblast.json",
            use_cache=use_cache
        )
        return AirRaidOblastStatuses(data)


__all__ = ('Client',)
