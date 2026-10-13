import unittest

from alerts_in_ua.alerts import Alerts
from tests.helpers import load_fixture


def ids(alerts):
    return sorted(alert.id for alert in alerts)


class AlertsTestCase(unittest.TestCase):

    def setUp(self):
        self.alerts = Alerts(load_fixture())

    def test_red_and_yellow_partition_all_alerts(self):
        red = ids(self.alerts.get_red_alerts())
        yellow = ids(self.alerts.get_yellow_alerts())
        self.assertEqual(red, [8757, 76016, 257385, 285526])
        self.assertEqual(yellow, [262473, 285567, 285589])
        self.assertEqual(sorted(red + yellow), ids(self.alerts))

    def test_get_alerts_by_alert_level(self):
        self.assertEqual(ids(self.alerts.get_alerts_by_alert_level("red")), ids(self.alerts.get_red_alerts()))
        self.assertEqual(self.alerts.get_alerts_by_alert_level("green"), [])

    def test_filter_by_alert_level(self):
        self.assertEqual(
            ids(self.alerts.filter("alert_level", "red", "alert_type", "artillery_shelling")),
            [76016, 257385],
        )

    def test_get_alerts_with_threat_type(self):
        self.assertEqual(ids(self.alerts.get_alerts_with_threat_type("drones")), [285567])
        self.assertEqual(ids(self.alerts.get_alerts_with_threat_type("unspecified_missiles")), [257385, 262473, 285526])
        self.assertEqual(self.alerts.get_alerts_with_threat_type("ballistic_missiles"), [])

    def test_existing_methods_still_work(self):
        self.assertEqual(len(self.alerts), 7)
        self.assertEqual(ids(self.alerts.get_artillery_shelling_alerts()), [76016, 257385])
        self.assertEqual(str(self.alerts.get_last_updated_at()), "2026-10-13 10:36:50+03:00")

    def test_empty_alert_list(self):
        alerts = Alerts({"alerts": [], "meta": {"last_updated_at": "2026/10/13 07:36:50 +0000"}})
        self.assertEqual(alerts.get_red_alerts(), [])
        self.assertEqual(alerts.get_alerts_with_threat_type("drones"), [])


if __name__ == "__main__":
    unittest.main()
