import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from alerts_in_ua import AsyncClient, Client
from alerts_in_ua.threat import Threat
from tests.helpers import load_fixture

LAST_MODIFIED = "Tue, 13 Oct 2026 07:36:50 GMT"


class ClientTestCase(unittest.TestCase):

    @patch("alerts_in_ua.client.requests.get")
    def test_get_active_alerts_parses_levels_and_threats(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            headers={"Last-Modified": LAST_MODIFIED},
            json=MagicMock(return_value=load_fixture()),
        )
        alerts = Client(token="test").get_active_alerts()
        self.assertTrue(mock_get.call_args[0][0].endswith("/v1/alerts/active.json"))
        self.assertEqual(len(alerts.get_red_alerts()), 4)
        self.assertEqual(len(alerts.get_yellow_alerts()), 3)
        self.assertTrue(all(isinstance(t, Threat) for a in alerts for t in a.threats))

    @patch("alerts_in_ua.client.requests.get")
    def test_cached_response_keeps_threats(self, mock_get):
        ok = MagicMock(status_code=200, headers={"Last-Modified": LAST_MODIFIED},
                       json=MagicMock(return_value=load_fixture()))
        mock_get.side_effect = [ok, MagicMock(status_code=304)]
        client = Client(token="test")
        client.get_active_alerts()
        alerts = client.get_active_alerts()
        self.assertEqual(mock_get.call_args[1]["headers"]["If-Modified-Since"], LAST_MODIFIED)
        self.assertEqual(len(alerts.get_alerts_with_threat_type("drones")), 1)


class AsyncClientTestCase(unittest.TestCase):

    def test_get_active_alerts_parses_levels_and_threats(self):
        response = MagicMock(status=200, headers={"Last-Modified": LAST_MODIFIED},
                             json=AsyncMock(return_value=load_fixture()))
        session = MagicMock(get=AsyncMock(return_value=response))
        session.__aenter__ = AsyncMock(return_value=session)
        session.__aexit__ = AsyncMock(return_value=False)
        with patch("alerts_in_ua.async_client.aiohttp.ClientSession", return_value=session):
            alerts = asyncio.run(AsyncClient(token="test").get_active_alerts())
        self.assertEqual(len(alerts.get_red_alerts()), 4)
        self.assertEqual(alerts.get_alerts_with_threat_type("drones")[0].threats[0].level, "yellow")


if __name__ == "__main__":
    unittest.main()
