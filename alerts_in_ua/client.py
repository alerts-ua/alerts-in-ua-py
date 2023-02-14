import requests
from .errors import UnauthorizedError, RateLimitError, InternalServerError, ForbiddenError
from .alert import Alert
from .alerts import Alerts
from .user_agent import UserAgent
from typing import List, Dict, Union

class Client:
    REQUEST_TIMEOUT = 5
    API_BASE_URL = "https://api.alerts.in.ua"
    def __init__(self, token: str):
        self.token = token
        self.base_url = Client.API_BASE_URL + "/v1/"

        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": UserAgent.get_user_agent()
        }
        self.cache = {}

    def _request(self, endpoint: str, use_cache=True):
        # Check if endpoint is in cache and return cached data if not modified
        if endpoint in self.cache and use_cache == True:
            cached_data = self.cache[endpoint]
            headers = {
                **self.headers,
                **{"If-Modified-Since": cached_data["Last-Modified"]},
            }
            response = requests.get(
                self.base_url + endpoint,
                headers=headers,
                timeout=Client.REQUEST_TIMEOUT,
            )
            if response.status_code == 304:
                return cached_data["Data"]

        # Make the request
        response = requests.get(
            self.base_url + endpoint,
            headers=self.headers,
            timeout=Client.REQUEST_TIMEOUT,
        )

        # Check if response is successful
        if response.status_code == 200:
            data = response.json()
            self.cache[endpoint] = {
                "Data": data,
                "Last-Modified": response.headers["Last-Modified"],
            }
            return data
        else:
            message = None
            try:
                data = response.json()
                json_message = data.get("message")
                message = f"{json_message} HTTP Code:{response.status_code}"
            except:
                pass
            if response.status_code == 401:
                if message is None:
                    message = "Unauthorized: Incorrect token"
                raise UnauthorizedError(message)
            elif response.status_code == 403:
                if message is None:
                    message = "Forbidden. API may not be available in some regions. Please ask api@alerts.in.ua for details."
                raise ForbiddenError(message)
            elif response.status_code == 429:
                if message is None:
                    message = "Too many requests: Rate limit exceeded"
                raise RateLimitError(message)
            elif response.status_code == 500:
                raise InternalServerError("Internal server error")
            else:
                raise ApiError(f"Unknown error. HTTP Code:{response.status_code}")

    def get_active_alerts(self, use_cache=True) -> Alerts:
        data = self._request("alerts/active.json", use_cache=use_cache)
        return Alerts(data)