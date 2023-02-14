import aiohttp
from .errors import UnauthorizedError, RateLimitError, InternalServerError, ForbiddenError
from .alert import Alert
from .alerts import Alerts
from .user_agent import UserAgent

class AsyncClient:
    REQUEST_TIMEOUT = 5
    API_BASE_URL = "https://api.alerts.in.ua"

    def __init__(self, token: str):
        self.token = token
        self.base_url = "/v1/"

        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": UserAgent.get_user_agent()
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

    async def get_active_alerts(self, use_cache=True):
        data = await self._request("alerts/active.json", use_cache=use_cache)
        return Alerts(data)
