import unittest

from alerts_in_ua.threat import Threat


class ThreatTestCase(unittest.TestCase):

    def setUp(self):
        self.data = {
            "threat_type": "drones",
            "level": "yellow",
            "started_at": "2026-10-13T07:12:05.123Z",
            "source_message": "Дронова загроза (жовтий рівень)",
        }

    def test_fields(self):
        threat = Threat(self.data)
        self.assertEqual(threat.threat_type, "drones")
        self.assertEqual(threat.level, "yellow")
        self.assertEqual(threat.source_message, "Дронова загроза (жовтий рівень)")

    def test_started_at_is_kyiv_time(self):
        threat = Threat(self.data)
        self.assertEqual(str(threat.started_at), "2026-10-13 10:12:05.123000+03:00")
        self.assertEqual(threat.started_at.tzinfo.zone, "Europe/Kyiv")

    def test_level_helpers(self):
        self.assertTrue(Threat(self.data).is_yellow())
        self.assertFalse(Threat(self.data).is_red())
        red = Threat({**self.data, "level": "red"})
        self.assertTrue(red.is_red())
        self.assertFalse(red.is_yellow())

    def test_missing_optional_fields(self):
        threat = Threat({"threat_type": "unknown"})
        self.assertIsNone(threat.level)
        self.assertIsNone(threat.started_at)
        self.assertIsNone(threat.source_message)
        self.assertFalse(threat.is_red())
        self.assertFalse(threat.is_yellow())

    def test_repr(self):
        threat = Threat({**self.data, "started_at": None})
        self.assertEqual(
            repr(threat),
            "Threat({'threat_type': 'drones', 'level': 'yellow', 'started_at': None, "
            "'source_message': 'Дронова загроза (жовтий рівень)'})",
        )


if __name__ == "__main__":
    unittest.main()
