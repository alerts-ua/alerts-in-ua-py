import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from alerts_in_ua import AsyncClient, Client
from alerts_in_ua.air_raid_alert_oblast_status import AirRaidAlertOblastStatus
from alerts_in_ua.air_raid_alert_oblast_statuses import AirRaidAlertOblastStatuses
from alerts_in_ua.air_raid_alert_status import AirRaidAlertStatus
from alerts_in_ua.air_raid_alert_status_resolver import AirRaidAlertStatusResolver

LAST_MODIFIED = "Tue, 13 Oct 2026 07:36:50 GMT"

# Captured from the live API at the same moment
BY_OBLAST_V1 = "APNPANNANAPPANNPPPNPAPNPPNP"
BY_OBLAST_V2 = "RPNPRNNRNYPPRNNPPPNPYPNPPNP"


def uid_string(statuses):
    """Builds an IoT status string with the given {uid: char}, 'N' elsewhere."""
    chars = [" "] + ["N"] * 40
    for uid, char in statuses.items():
        chars[uid] = char
    return "".join(chars)


def ok_response(data):
    return MagicMock(status_code=200, headers={"Last-Modified": LAST_MODIFIED},
                     json=MagicMock(return_value=data))


class ResolverTestCase(unittest.TestCase):

    def test_v2_chars_resolve_to_active_with_level(self):
        resolved = AirRaidAlertStatusResolver.resolve_status_string(
            uid_string({16: "R", 31: "Y", 14: "P"}), {16: "Луганська область", 31: "м. Київ", 14: "Київська область"}
        )
        by_uid = {r["uid"]: r for r in resolved}
        self.assertEqual((by_uid[16]["status"], by_uid[16]["alert_level"]), ("active", "red"))
        self.assertEqual((by_uid[31]["status"], by_uid[31]["alert_level"]), ("active", "yellow"))
        self.assertEqual((by_uid[14]["status"], by_uid[14]["alert_level"]), ("partly", None))

    def test_v1_active_has_no_level(self):
        self.assertEqual(AirRaidAlertStatusResolver.resolve_status_char("A"), "active")
        self.assertIsNone(AirRaidAlertStatusResolver.resolve_level_char("A"))


class StatusModelsTestCase(unittest.TestCase):

    def test_status_levels_and_repr(self):
        red = AirRaidAlertStatus("Луганська область", "active", 16, alert_level="red")
        yellow = AirRaidAlertStatus("м. Київ", "active", 31, alert_level="yellow")
        v1 = AirRaidAlertStatus("м. Київ", "active", 31)
        self.assertTrue(red.is_red() and not red.is_yellow())
        self.assertTrue(yellow.is_yellow() and not yellow.is_red())
        self.assertFalse(v1.is_red() or v1.is_yellow())
        self.assertEqual(repr(red), "🔴 Луганська область")
        self.assertEqual(repr(yellow), "🟠 м. Київ")
        self.assertEqual(repr(v1), "🔴 м. Київ")

    def test_oblast_status_v2(self):
        red = AirRaidAlertOblastStatus("Луганська область", "R")
        yellow = AirRaidAlertOblastStatus("м. Київ", "Y")
        self.assertTrue(red.is_active_on_all_oblast() and red.is_red())
        self.assertTrue(yellow.is_active_on_all_oblast() and yellow.is_yellow())
        self.assertIsNone(AirRaidAlertOblastStatus("x", "A").alert_level)
        self.assertTrue(AirRaidAlertOblastStatus("x", "P", oblast_level_only=True).is_no_alert())

    def test_oblast_statuses_v2_matches_v1_status(self):
        v1 = AirRaidAlertOblastStatuses(BY_OBLAST_V1)
        v2 = AirRaidAlertOblastStatuses(BY_OBLAST_V2)
        self.assertEqual(len(v2), 27)
        self.assertEqual([s.status for s in v1], [s.status for s in v2])
        self.assertEqual(len(v2.get_red_alert_oblasts()), 4)
        self.assertEqual(len(v2.get_yellow_alert_oblasts()), 2)
        self.assertEqual(len(v2.get_red_alert_oblasts()) + len(v2.get_yellow_alert_oblasts()),
                         len(v2.get_active_alert_oblasts()))
        self.assertEqual(v1.get_red_alert_oblasts(), [])


class ClientIotTestCase(unittest.TestCase):

    @patch("alerts_in_ua.client.requests.get")
    def test_statuses_default_to_v1(self, mock_get):
        mock_get.return_value = ok_response(uid_string({31: "A"}))
        statuses = Client(token="test").get_air_raid_alert_statuses()
        self.assertTrue(mock_get.call_args[0][0].endswith("/v1/iot/active_air_raid_alerts.json"))
        self.assertEqual(statuses.get_status(31).status, "active")
        self.assertIsNone(statuses.get_status(31).alert_level)

    @patch("alerts_in_ua.client.requests.get")
    def test_statuses_v2(self, mock_get):
        mock_get.return_value = ok_response(uid_string({16: "R", 31: "Y"}))
        statuses = Client(token="test").get_air_raid_alert_statuses(include_alert_level=True)
        self.assertEqual(mock_get.call_args[0][0], "https://api.alerts.in.ua/v2/iot/active_air_raid_alerts.json")
        self.assertEqual([s.uid for s in statuses.get_red_alert_statuses()], [16])
        self.assertEqual([s.uid for s in statuses.get_yellow_alert_statuses()], [31])
        self.assertEqual(len(statuses.get_active_alert_statuses()), 2)

    @patch("alerts_in_ua.client.requests.get")
    def test_single_status_and_by_oblast_v2(self, mock_get):
        client = Client(token="test")
        mock_get.return_value = ok_response("Y")
        status = client.get_air_raid_alert_status(31, include_alert_level=True)
        self.assertEqual(mock_get.call_args[0][0], "https://api.alerts.in.ua/v2/iot/active_air_raid_alerts/31.json")
        self.assertTrue(status.is_yellow())
        mock_get.return_value = ok_response(BY_OBLAST_V2)
        oblasts = client.get_air_raid_alert_statuses_by_oblast(include_alert_level=True)
        self.assertEqual(mock_get.call_args[0][0], "https://api.alerts.in.ua/v2/iot/active_air_raid_alerts_by_oblast.json")
        self.assertEqual(len(oblasts.get_red_alert_oblasts()), 4)

    @patch("alerts_in_ua.client.requests.get")
    def test_v1_and_v2_are_cached_separately(self, mock_get):
        mock_get.side_effect = [ok_response("A"), ok_response("R")]
        client = Client(token="test")
        client.get_air_raid_alert_status(31)
        status = client.get_air_raid_alert_status(31, include_alert_level=True)
        self.assertNotIn("If-Modified-Since", mock_get.call_args[1]["headers"])
        self.assertTrue(status.is_red())
        self.assertIn("v2/iot/active_air_raid_alerts/31.json", client.cache)

    @patch("alerts_in_ua.client.requests.get")
    def test_include_alert_level_false_uses_v1(self, mock_get):
        mock_get.return_value = ok_response("A")
        status = Client(token="test").get_air_raid_alert_status(31, include_alert_level=False)
        self.assertTrue(mock_get.call_args[0][0].endswith("/v1/iot/active_air_raid_alerts/31.json"))
        self.assertTrue(status.is_active_on_all_oblast())
        self.assertIsNone(status.alert_level)


class AsyncClientIotTestCase(unittest.TestCase):

    def test_statuses_v2(self):
        response = MagicMock(status=200, headers={"Last-Modified": LAST_MODIFIED},
                             json=AsyncMock(return_value=uid_string({16: "R", 31: "Y"})))
        session = MagicMock(get=AsyncMock(return_value=response))
        session.__aenter__ = AsyncMock(return_value=session)
        session.__aexit__ = AsyncMock(return_value=False)
        with patch("alerts_in_ua.async_client.aiohttp.ClientSession", return_value=session):
            statuses = asyncio.run(AsyncClient(token="test").get_air_raid_alert_statuses(include_alert_level=True))
        self.assertEqual(session.get.call_args[0][0], "/v2/iot/active_air_raid_alerts.json")
        self.assertTrue(statuses.get_status(16).is_red())
        self.assertTrue(statuses.get_status(31).is_yellow())


if __name__ == "__main__":
    unittest.main()
