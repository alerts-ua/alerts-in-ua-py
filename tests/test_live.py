"""Live checks against api.alerts.in.ua. Skipped unless ALERTS_IN_UA_TOKEN is set."""
import asyncio
import os
import unittest

from alerts_in_ua import AsyncClient, Client
from alerts_in_ua.threat import Threat

TOKEN = os.environ.get("ALERTS_IN_UA_TOKEN")
LEVELS = {"red", "yellow"}
THREAT_TYPES = {
    "tactic_aircraft_activity", "strategic_aircraft_activity", "mig31k_departure", "ballistic_missiles",
    "cruise_missiles", "unspecified_missiles", "drones", "guided_aerial_bombs", "air_defense", "unknown",
}


@unittest.skipUnless(TOKEN, "set ALERTS_IN_UA_TOKEN to run live API tests")
class LiveTestCase(unittest.TestCase):

    def check_alerts(self, alerts):
        self.assertGreater(len(alerts), 0)
        for alert in alerts:
            self.assertIn(alert.alert_level, LEVELS, alert)
            self.assertIsInstance(alert.threats, list)
            for threat in alert.threats:
                self.assertIsInstance(threat, Threat)
                self.assertIn(threat.threat_type, THREAT_TYPES, threat)
                self.assertIn(threat.level, LEVELS, threat)
                self.assertIsNotNone(threat.started_at, threat)
        self.assertEqual(
            len(alerts.get_red_alerts()) + len(alerts.get_yellow_alerts()), len(alerts)
        )

    def test_active_alerts(self):
        self.check_alerts(Client(token=TOKEN).get_active_alerts(use_cache=False))

    def test_active_alerts_async(self):
        alerts = asyncio.run(AsyncClient(token=TOKEN).get_active_alerts(use_cache=False))
        self.check_alerts(alerts)

    def check_iot_v2_statuses(self, statuses):
        self.assertGreater(len(statuses), 0)
        for status in statuses:
            if status.status == "active":
                self.assertIn(status.alert_level, LEVELS, status)
            else:
                self.assertIsNone(status.alert_level, status)

    def test_iot_v2_statuses(self):
        self.check_iot_v2_statuses(Client(token=TOKEN).get_air_raid_alert_statuses(use_cache=False, api_version=2))

    def test_iot_v2_statuses_async(self):
        statuses = asyncio.run(AsyncClient(token=TOKEN).get_air_raid_alert_statuses(use_cache=False, api_version=2))
        self.check_iot_v2_statuses(statuses)

    def test_iot_v2_by_oblast_and_single_status(self):
        client = Client(token=TOKEN)
        oblasts = client.get_air_raid_alert_statuses_by_oblast(use_cache=False, api_version=2)
        self.assertEqual(len(oblasts), 27)
        self.check_iot_v2_statuses(oblasts)
        status = client.get_air_raid_alert_status(31, use_cache=False, api_version=2)
        self.assertEqual(status.location_title, "м. Київ")
        self.check_iot_v2_statuses([status])

    def test_iot_v1_has_no_levels(self):
        statuses = Client(token=TOKEN).get_air_raid_alert_statuses(use_cache=False)
        self.assertTrue(all(s.alert_level is None for s in statuses))


if __name__ == "__main__":
    unittest.main()
