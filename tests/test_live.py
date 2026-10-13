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


if __name__ == "__main__":
    unittest.main()
