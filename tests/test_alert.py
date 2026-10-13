import unittest

from alerts_in_ua.alert import Alert
from alerts_in_ua.threat import Threat
from tests.helpers import load_fixture, alert_by_id


class AlertTestCase(unittest.TestCase):

    def setUp(self):
        self.data = load_fixture()

    def test_basic_fields(self):
        alert = Alert(alert_by_id(self.data, 8757))
        self.assertEqual(alert.id, 8757)
        self.assertEqual(alert.location_title, "Луганська область")
        self.assertEqual(alert.location_title_en, "Luhansk Oblast")
        self.assertEqual(alert.location_type, "oblast")
        self.assertEqual(alert.alert_type, "air_raid")
        self.assertEqual(alert.location_uid, "16")
        self.assertIsNone(alert.country)
        self.assertFalse(alert.is_finished())

    def test_red_alert_with_threat(self):
        alert = Alert(alert_by_id(self.data, 285526))
        self.assertEqual(alert.alert_level, "red")
        self.assertTrue(alert.is_red())
        self.assertFalse(alert.is_yellow())
        self.assertTrue(alert.has_threats())
        self.assertEqual(len(alert.threats), 1)
        threat = alert.threats[0]
        self.assertIsInstance(threat, Threat)
        self.assertEqual(threat.threat_type, "unspecified_missiles")
        self.assertTrue(threat.is_red())
        self.assertEqual(threat.source_message, "Ракетна загроза (червоний рівень)")
        self.assertEqual(threat.started_at.tzinfo.zone, "Europe/Kyiv")

    def test_threat_without_source_message(self):
        alert = Alert(alert_by_id(self.data, 257385))
        self.assertEqual(alert.alert_type, "artillery_shelling")
        self.assertIsNone(alert.threats[0].source_message)

    def test_yellow_alert_with_drones(self):
        alert = Alert(alert_by_id(self.data, 285567))
        self.assertTrue(alert.is_yellow())
        self.assertEqual([t.threat_type for t in alert.threats], ["drones"])
        self.assertEqual(len(alert.get_threats_by_type("drones")), 1)
        self.assertEqual(alert.get_threats_by_type("ballistic_missiles"), [])

    def test_threat_level_is_independent_of_alert_level(self):
        # Seen in production: a yellow alert can carry a red threat.
        alert = Alert(alert_by_id(self.data, 262473))
        self.assertTrue(alert.is_yellow())
        self.assertTrue(alert.threats[0].is_red())

    def test_threats_absent_is_empty_list(self):
        raw = alert_by_id(self.data, 285589)
        self.assertNotIn("threats", raw)
        alert = Alert(raw)
        self.assertEqual(alert.threats, [])
        self.assertFalse(alert.has_threats())
        self.assertTrue(alert.is_yellow())

    def test_threats_null_is_empty_list(self):
        raw = alert_by_id(self.data, 285589)
        raw["threats"] = None
        self.assertEqual(Alert(raw).threats, [])

    def test_legacy_payload_without_level(self):
        raw = alert_by_id(self.data, 8757)
        del raw["alert_level"]
        alert = Alert(raw)
        self.assertIsNone(alert.alert_level)
        self.assertFalse(alert.is_red())
        self.assertFalse(alert.is_yellow())
        self.assertEqual(alert.threats, [])

    def test_repr_includes_level_and_threats(self):
        alert = Alert(alert_by_id(self.data, 285567))
        text = repr(alert)
        self.assertTrue(text.startswith("Alert({'id': 285567, "))
        self.assertTrue(text.endswith("})"))
        self.assertIn("'alert_level': 'yellow'", text)
        self.assertIn("'threats': [Threat({'threat_type': 'drones', 'level': 'yellow', ", text)
        self.assertIn("'location_title_en': ", text)
        self.assertIn("'country': None", text)


if __name__ == "__main__":
    unittest.main()
